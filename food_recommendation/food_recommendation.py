import pandas as pd
from config import ConnPath
import psycopg2


class FoodRecommendation():

    @staticmethod
    def user_type_recommendation():
        sql_food_order_connect=ConnPath().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        no_of_days, user_no_of_days = ConnPath.no_of_days()

        user_type_table=pd.read_sql((f"""SELECT
                fo.uid,
                SUM(CASE WHEN fl.type = 'VEG' THEN 1 ELSE 0 END) AS veg_count,
                SUM(CASE WHEN fl.type = 'NON_VEG' THEN 1 ELSE 0 END) AS non_veg_count,
                SUM(CASE WHEN fl.type = 'EGG' THEN 1 ELSE 0 END) AS egg_count,
                SUM(CASE WHEN fl.type = 'OTHER' THEN 1 ELSE 0 END) AS other_count
            FROM
                gintaa_food_order.food_order fo
            LEFT JOIN
                gintaa_food_order.food_order_details fod ON fo.id = fod.food_order_id
            LEFT JOIN
                gintaa_food_order.food_listing fl ON fod.food_listing_id = fl.id
            WHERE
                fo.order_status = 'DELIVERED'
                AND fo.created_date >= CURRENT_DATE - INTERVAL '{user_no_of_days} day' 
                AND fo.created_date < CURRENT_DATE
            GROUP BY
                fo.uid"""), conn_food_order)
        user_type_df=pd.DataFrame(data=user_type_table,index=None)

        return user_type_df

    
    @staticmethod
    def popular_food():
        sql_food_order_connect=ConnPath().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        sql_food_listing_connect = ConnPath().food_listing_sql_config()
        conn_food_listing = psycopg2.connect(database=sql_food_listing_connect["database"], user = sql_food_listing_connect["user"], password = sql_food_listing_connect["password"], host = sql_food_listing_connect["host"], port = sql_food_listing_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_listing)

        no_of_days, user_no_of_days = ConnPath.no_of_days()
        
        food_id_table = pd.read_sql((f"SELECT food_order_id,food_listing_id FROM gintaa_food_order.food_order_details where created_date >= CURRENT_DATE - INTERVAL '{no_of_days} days'"), conn_food_order)
        food_id_df = pd.DataFrame(data=food_id_table,index=None)
        
        food_listing_txns = food_id_df['food_listing_id'].value_counts().reset_index()
        food_listing_txns.columns = ['food_listing_id', 'txns_count']
        food_listing_id_lst=food_id_df['food_listing_id'].unique().tolist()
        formatted_food_listing_ids = ", ".join(f"'{id_}'" for id_ in food_listing_id_lst)

        food_listing_table=pd.read_sql((f"SELECT fl.id as food_listing_id, fl.name as food_name,fl.image_url,fl.description,fl.avg_rating,r.name, COALESCE(fl.cuisine, rc.cuisine_id) as cuisine, r.rid, r.location, r.created_date,DATE_PART('day', NOW() - r.created_date) AS no_of_days, rc.cuisine_id FROM gintaa_food_listing.restaurant as r INNER JOIN gintaa_food_listing.food_listing as fl ON fl.rid = r.rid left JOIN gintaa_food_listing.restaurant_cuisine as rc on fl.rid=rc.rid WHERE COALESCE(r.blacklisted, false) = false and rc.cuisine_type='MAIN' AND image_url is not null"), conn_food_listing)
        food_listing_df=pd.DataFrame(data=food_listing_table,index=None)

        rhi_table = pd.read_sql(("select rid, score as rhi_score from gintaa_food_listing.restaurant_health_index"), conn_food_listing)
        rhi_df = pd.DataFrame(data=rhi_table,index=None)

        food_listing_df = pd.merge(food_listing_df, food_listing_txns, on='food_listing_id')
        food_listing_df = pd.merge(food_listing_df, rhi_df, on='rid')
        food_listing_df['description_word_count'] = food_listing_df['description'].apply(lambda x: len([word for word in str(x).replace(',', ' ').split() if word.lower() not in ['veg', 'non', 'half', 'full','nonveg']]) if pd.notnull(x) else 0)
        food_listing_df.loc[food_listing_df['no_of_days'] < 30, 'avg_txns'] = food_listing_df['txns_count'] / food_listing_df['no_of_days']
        food_listing_df.loc[food_listing_df['no_of_days'] >= 30, 'avg_txns'] = food_listing_df['txns_count'] / 30
        max_txns = max(food_listing_df["avg_txns"])
        food_listing_df["txns_score"] = 0
        food_listing_df['image_score'] = 0
        food_listing_df['description_score'] = 0
        food_listing_df["txns_score"] = (food_listing_df['avg_txns']/max_txns)*30
        food_listing_df.loc[food_listing_df['image_url'].notnull(), 'image_score'] = 20
        food_listing_df.loc[food_listing_df['description_word_count'] > 10, 'description_score'] = 10
        food_listing_df.loc[(food_listing_df['description_word_count'] <= 10) & (food_listing_df['description_word_count'] >= 3), 'description_score'] = 5
        food_listing_df["rating_score"] = food_listing_df["avg_rating"].apply(lambda x: x * 2 if x >= 3 else 0)
        food_listing_df['rhi_score'] = food_listing_df['rhi_score']*0.3
        food_listing_df['score'] = food_listing_df["txns_score"]+food_listing_df['image_score']+food_listing_df['description_score']+food_listing_df["rating_score"]+food_listing_df['rhi_score']
        food_listing_df['score'] = food_listing_df['score'].round(3).astype(float)
        key_columns = ['food_listing_id', 'food_name', 'name', 'cuisine', 'rid','score']
        unique_df=food_listing_df[key_columns]
        unique_df = unique_df.drop_duplicates(subset=key_columns, keep='first')

        return unique_df
    
    @staticmethod
    def user_cuisine_recommendation():
        sql_food_order_connect=ConnPath().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        sql_food_listing_connect=ConnPath().food_listing_sql_config()
        conn_food_listing = psycopg2.connect(database=sql_food_listing_connect["database"], user = sql_food_listing_connect["user"], password = sql_food_listing_connect["password"], host = sql_food_listing_connect["host"], port = sql_food_listing_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_listing)

        no_of_days, user_no_of_days = ConnPath.no_of_days()

        food_order_table=pd.read_sql((f"SELECT uid,id as food_order_id,created_date,delivery_address,rid FROM gintaa_food_order.food_order where order_status='DELIVERED' and created_date >= CURRENT_DATE - INTERVAL '{no_of_days} days'"), conn_food_order)
        food_order_df=pd.DataFrame(data=food_order_table,index=None)
        uid_address_df=food_order_df[['uid','created_date','delivery_address']]
        uid_address_df['created_date'] = pd.to_datetime(uid_address_df['created_date'])
        uid_address_df.sort_values(['uid', 'created_date'], ascending=[True, False], inplace=True)
        uid_address_df.drop_duplicates('uid', keep='first', inplace=True)
        uid_address_df=uid_address_df[['uid','delivery_address']]

        food_id_table=pd.read_sql((f"SELECT food_order_id,food_listing_id FROM gintaa_food_order.food_order_details where created_date >= CURRENT_DATE - INTERVAL '{no_of_days} days'"), conn_food_order)
        food_id_df=pd.DataFrame(data=food_id_table,index=None)

        food_listing_txns = food_id_df['food_listing_id'].value_counts().reset_index()
        food_listing_txns.columns = ['food_listing_id', 'txns_count']

        food_listing_id_lst=food_id_df['food_listing_id'].unique().tolist()
        formatted_food_listing_ids = ", ".join(f"'{id_}'" for id_ in food_listing_id_lst)
        food_listing_table=pd.read_sql((f"SELECT fl.id as food_listing_id, fl.name as food_name, COALESCE(fl.cuisine, rc.cuisine_id) as cuisine, r.rid, r.location, rc.cuisine_type FROM gintaa_food_listing.restaurant as r INNER JOIN gintaa_food_listing.food_listing as fl ON fl.rid = r.rid left JOIN gintaa_food_listing.restaurant_cuisine as rc on r.rid=rc.rid where COALESCE(r.blacklisted, false) = false AND fl.id IN ({formatted_food_listing_ids})"), conn_food_listing)
        food_listing_df=pd.DataFrame(data=food_listing_table,index=None)
        rid_food_listing_df=food_listing_df[['rid','food_listing_id','cuisine']]

        rid_food_listing_df=pd.merge(rid_food_listing_df, food_listing_txns, on='food_listing_id',how='left')

        rid_txns = food_order_df['rid'].value_counts().reset_index()
        rid_txns.columns = ['rid', 'txns_count']

        category_rid_df=food_listing_df.groupby('cuisine')['rid'].unique().reset_index()
        category_rid_df = category_rid_df.rename(columns={'rid': 'rid_list'})

        merged_df = pd.merge(food_order_df, food_id_df, on='food_order_id') 
        merged_df=pd.merge(merged_df,food_listing_df,on='food_listing_id')
        df=merged_df[['uid','created_date','cuisine']]

        category_id_count = df.groupby(['uid', 'cuisine']).size().reset_index().rename(columns={0: 'count'})
        max_counts = category_id_count.groupby('uid')['count'].max().reset_index()
        max_category_id_count = pd.merge(category_id_count, max_counts, on=['uid', 'count'], how='inner')

        date_idx=df.groupby(['uid', 'cuisine'])['created_date'].idxmax()
        latest_dates = df.loc[date_idx]

        output_df=pd.merge(max_category_id_count, latest_dates, on=['uid', 'cuisine'], how='left')

        idx = output_df.groupby('uid')['created_date'].idxmax()
        filtered_df = output_df.loc[idx]

        filtered_df=pd.merge(category_rid_df,filtered_df,on='cuisine',how='right')

        return filtered_df