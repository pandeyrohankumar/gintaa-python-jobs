import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from config import CONN_PATH

class RHI_DATASET():
    def create_dataset(self):
        sql_food_order_connect=CONN_PATH().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        sql_food_listing_connect=CONN_PATH().food_listing_sql_config()
        conn_food_listing = psycopg2.connect(database=sql_food_listing_connect["database"], user = sql_food_listing_connect["user"], password = sql_food_listing_connect["password"], host = sql_food_listing_connect["host"], port = sql_food_listing_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_listing)

        time_period=CONN_PATH().time_period()

        thirty_days_ago = datetime.now() - timedelta(days=int(time_period))
        thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')

        main_table=pd.read_sql((f"SELECT fo.id as order_id, fo.order_status, fo.rid, fo.delivery_type, fostl.next_state_id, fostl.created_date  FROM gintaa_food_order.food_order_status_transition_log as fostl inner join gintaa_food_order.food_order as fo on fostl.order_id=fo.id where fostl.created_date>= '{thirty_days_ago_str}'"), conn_food_order)
        main_df=pd.DataFrame(data=main_table,index=None)

        df=main_df[main_df["order_status"] == "DELIVERED"]
        df=df.drop("order_status", axis=1)

        delivery_time_df = df[df['next_state_id'] == 'DELIVERED'][['order_id', 'created_date']]
        delivery_time_df=delivery_time_df.rename(columns={'created_date': 'delivery_time'})
        df['created_date'] = pd.to_datetime(df['created_date'])
        df['time_diff'] = df.groupby(['order_id', 'rid','delivery_type'])['created_date'].diff().dt.total_seconds()

        result = df.pivot_table(index=['order_id', 'rid','delivery_type'], columns='next_state_id', values='time_diff').reset_index()

        result = result[['order_id', 'rid','delivery_type', 'ACCEPTED', 'PREPARED', 'DELIVERED']]
        result.columns = ['order_id', 'rid','delivery_type', 'PLACED-ACCEPTED', 'ACCEPTED-PREPARED', 'PREPARED-DELIVERED']

        result.columns.name = None
        result.columns = [f'{col[0]}-{col[1]}' if isinstance(col, tuple) else col for col in result.columns]
        max_time=720*60
        result = result[(result['PLACED-ACCEPTED'] <= max_time) & (result['ACCEPTED-PREPARED'] <= max_time) & (result['PREPARED-DELIVERED'] <= max_time)]
        avg_rating_table=pd.read_sql(("SELECT rid,delivery_time as rest_delivery_time, name as restaurant_name,created_date as restaurant_created_date,avg_rating as restaurant_avg_rating,blacklisted FROM gintaa_food_listing.restaurant"), conn_food_listing)
        avg_rating_df=pd.DataFrame(data=avg_rating_table,index=None)
        blacklisted_rids_df = avg_rating_df.loc[avg_rating_df['blacklisted'] == True, ['rid', 'restaurant_created_date']]
        avg_rating_df=avg_rating_df[avg_rating_df['blacklisted'] != True]

        result=pd.merge(result,avg_rating_df,on='rid',how='inner')
        result['self_delivery']= result['delivery_type'] == 'SELF'
        result.loc[result['PLACED-ACCEPTED'] <= 10, 'PLACED-ACCEPTED-SCORE'] = 20
        result.loc[(result['PLACED-ACCEPTED'] > 10) & (result['PLACED-ACCEPTED'] <= 180), 'PLACED-ACCEPTED-SCORE'] = 15
        result.loc[(result['PLACED-ACCEPTED'] > 180) & (result['PLACED-ACCEPTED'] <= 300), 'PLACED-ACCEPTED-SCORE'] = 10
        result.loc[(result['PLACED-ACCEPTED'] > 300) , 'PLACED-ACCEPTED-SCORE'] = 0

        result['ACCEPTED-PREPARED-SCORE'] = [
            (30 if not row['self_delivery'] and 180 <= row['ACCEPTED-PREPARED'] <= 900
            else 15 if not row['self_delivery'] and 900 < row['ACCEPTED-PREPARED'] <= 1800
            else 10 if row['self_delivery'] and 180 <= row['ACCEPTED-PREPARED'] <= 900
            else 5 if row['self_delivery'] and 900 < row['ACCEPTED-PREPARED'] <= 1800
            else 0)
            for index, row in result.iterrows()
        ]
        
        result['PREPARED-DELIVERED-SCORE'] = [
            (20 if row['self_delivery'] and pd.isna(row['rest_delivery_time']) and 300 <= row['PREPARED-DELIVERED'] <= 1500
            else 15 if row['self_delivery'] and pd.isna(row['rest_delivery_time']) and 1500 < row['PREPARED-DELIVERED'] <= 2100
            else 10 if row['self_delivery'] and pd.isna(row['rest_delivery_time']) and 2100 < row['PREPARED-DELIVERED'] <= 2700
            else 0 if row['self_delivery'] and pd.isna(row['rest_delivery_time'])
            else 20 if row['self_delivery'] and 300 <= row['PREPARED-DELIVERED'] <= (row['rest_delivery_time']/3)
            else 15 if row['self_delivery'] and (row['rest_delivery_time']/3) < row['PREPARED-DELIVERED'] <= (row['rest_delivery_time']/2)
            else 10 if row['self_delivery'] and (row['rest_delivery_time']/2) < row['PREPARED-DELIVERED'] <= row['rest_delivery_time']
            else 0)
            for index, row in result.iterrows()
        ]

        result.drop('PLACED-ACCEPTED', axis=1, inplace=True)
        result.drop('ACCEPTED-PREPARED', axis=1, inplace=True)
        result.drop('PREPARED-DELIVERED', axis=1, inplace=True)

        result=pd.merge(result,delivery_time_df,on='order_id',how='left')
        result=result.sort_values(by=['rid', 'delivery_time'])

        placed_accepted_result_values = {}
        placed_accepted_prev_result = {}

        accepted_prepared_result_values = {}
        accepted_prepared_prev_result = {}

        prepared_delivered_result_values = {}
        prepared_delivered_prev_result = {}

        for index,row in result.iterrows():
            rid = row['rid']
            if rid not in placed_accepted_result_values:
                placed_accepted_result_values[rid] = [row['PLACED-ACCEPTED-SCORE']]
                placed_accepted_prev_result[rid] = row['PLACED-ACCEPTED-SCORE']
            else:
                placed_accepted_result_values[rid].append((placed_accepted_prev_result[rid] + row['PLACED-ACCEPTED-SCORE']) / 2)
                placed_accepted_prev_result[rid] = (placed_accepted_prev_result[rid] + row['PLACED-ACCEPTED-SCORE']) / 2

            if rid not in accepted_prepared_result_values:
                accepted_prepared_result_values[rid] = [row['ACCEPTED-PREPARED-SCORE']]
                accepted_prepared_prev_result[rid] = row['ACCEPTED-PREPARED-SCORE']
            else:
                accepted_prepared_result_values[rid].append((accepted_prepared_prev_result[rid] + row['ACCEPTED-PREPARED-SCORE']) / 2)
                accepted_prepared_prev_result[rid] = (accepted_prepared_prev_result[rid] + row['ACCEPTED-PREPARED-SCORE']) / 2

            if rid not in prepared_delivered_result_values:
                prepared_delivered_result_values[rid] = [row['PREPARED-DELIVERED-SCORE']]
                prepared_delivered_prev_result[rid] = row['PREPARED-DELIVERED-SCORE']
            else:
                prepared_delivered_result_values[rid].append((prepared_delivered_prev_result[rid] + row['PREPARED-DELIVERED-SCORE']) / 2)
                prepared_delivered_prev_result[rid] = (prepared_delivered_prev_result[rid] + row['PREPARED-DELIVERED-SCORE']) / 2

        result['PLACED-ACCEPTED-AVG-SCORE'] = result.apply(lambda row: '{:.3f}'.format(placed_accepted_result_values[row['rid']].pop(0)), axis=1) 
        result['ACCEPTED-PREPARED-AVG-SCORE'] = result.apply(lambda row: '{:.3f}'.format(accepted_prepared_result_values[row['rid']].pop(0)), axis=1)
        result['PREPARED-DELIVERED-AVG-SCORE'] = result.apply(lambda row: '{:.3f}'.format(prepared_delivered_result_values[row['rid']].pop(0)), axis=1)

        counts = result['rid'].value_counts().rename('No-of_orders_delivered')
        counts_df = pd.DataFrame({'rid': counts.index, 'No-of_orders_delivered': counts.values})

        result.drop_duplicates(subset='rid', keep='last', inplace=True)
        result = pd.merge(result, counts_df, on='rid',how='left')

        total_order_count = main_df[main_df['next_state_id'] == 'PLACED'].groupby('rid').size().reset_index(name='total_order_count')

        result=pd.merge(result,total_order_count,on='rid',how='left')

        return result,blacklisted_rids_df