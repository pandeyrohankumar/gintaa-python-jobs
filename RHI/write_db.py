import psycopg2
from config import CONN_PATH
from datetime import datetime
import pandas as pd
from google.cloud import bigquery


class WRITE_DB():
    def write_to_bq(self,df,blacklisted_df):
        
        client ,bq_table_name=CONN_PATH().big_query_conn()
        current_time = datetime.now()
        blacklisted_rids_df=pd.DataFrame(columns=['id', 'rid', 'number_of_orders_delivered', 'number_of_orders_placed', 'percentage_of_order_fulfilled', 'avg_rating', 'placed_accepted_score', 'accepted_prepared_score', 'prepared_delivered_score','avg_rating_score', 'percentage_order_fulfilled_score', 'score', 'restaurant_created_date', 'created_date'])
        blacklisted_rids_df['id']=blacklisted_df['rid'].astype(str)
        blacklisted_rids_df['rid']=blacklisted_df['rid'].astype(str)
        blacklisted_rids_df['number_of_orders_delivered']=0
        blacklisted_rids_df['number_of_orders_placed']=0
        blacklisted_rids_df['percentage_of_order_fulfilled']=0
        blacklisted_rids_df['avg_rating']=0
        blacklisted_rids_df['placed_accepted_score']=0
        blacklisted_rids_df['accepted_prepared_score']=0
        blacklisted_rids_df['prepared_delivered_score']=0
        blacklisted_rids_df['avg_rating_score']=0
        blacklisted_rids_df['percentage_order_fulfilled_score']=0
        blacklisted_rids_df['score']=0
        blacklisted_rids_df['restaurant_created_date']=blacklisted_df["restaurant_created_date"]
        blacklisted_rids_df['created_date']=current_time
        blacklisted_rows_to_insert = blacklisted_rids_df.to_dict(orient='records')
        blacklisted_rids_df = blacklisted_rids_df.where(pd.notna(blacklisted_rids_df), None)
        for record in blacklisted_rows_to_insert:
            record['restaurant_created_date'] = record['restaurant_created_date'].strftime('%Y-%m-%d %H:%M:%S')
            record['created_date'] = record['created_date'].strftime('%Y-%m-%d %H:%M:%S')
        
        bqdf = pd.DataFrame(columns=['id', 'rid', 'number_of_orders_delivered', 'number_of_orders_placed', 'percentage_of_order_fulfilled', 'avg_rating', 'placed_accepted_score', 'accepted_prepared_score', 'prepared_delivered_score','avg_rating_score', 'percentage_order_fulfilled_score', 'score', 'restaurant_created_date', 'created_date'])
        bqdf['id']=df["rid"].astype(str)
        bqdf['rid']=df["rid"].astype(str)
        bqdf['number_of_orders_delivered']=df["No-of_orders_delivered"].astype(int)
        bqdf['number_of_orders_placed']=df["total_order_count"].astype(int)
        bqdf['percentage_of_order_fulfilled']=df["PercentageOrderFulfilled"]
        bqdf['avg_rating']=df["restaurant_avg_rating"].astype(float)
        bqdf['placed_accepted_score']=df["PLACED-ACCEPTED-AVG-SCORE"].astype(float)
        bqdf['accepted_prepared_score']=df["ACCEPTED-PREPARED-AVG-SCORE"].astype(float)
        bqdf['prepared_delivered_score']=df["PREPARED-DELIVERED-AVG-SCORE"].astype(float)
        bqdf['avg_rating_score']=df["restaurant_avg_rating-score"].astype(float)
        bqdf['percentage_order_fulfilled_score']=df["PercentageOrderFulfilled-score"].astype(float)
        bqdf['score']=df["score"].astype(float)
        bqdf['restaurant_created_date']=df["restaurant_created_date"]
        bqdf['created_date']=current_time
        bqdf = bqdf.where(pd.notna(bqdf), None)
        rows_to_insert = bqdf.to_dict(orient='records')
        for record in rows_to_insert:
            record['restaurant_created_date'] = record['restaurant_created_date'].strftime('%Y-%m-%d %H:%M:%S')
            record['created_date'] = record['created_date'].strftime('%Y-%m-%d %H:%M:%S')


        client.insert_rows_json(bq_table_name, rows_to_insert)
        client.insert_rows_json(bq_table_name, blacklisted_rows_to_insert)

        
        return 'Write to BQ Done'


    def write_to_db(self,df,blacklisted_rids):
        sql_connect=CONN_PATH().food_listing_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        con = conn.cursor()
        for row in df.index:
            
            query = """
                INSERT INTO gintaa_food_listing.restaurant_health_index (id, rid,number_of_orders_delivered , placed_accepted_score ,accepted_prepared_score , prepared_delivered_score ,avg_rating_score, percentage_order_fulfilled_score , score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    rid=EXCLUDED.rid,
                    number_of_orders_delivered=EXCLUDED.number_of_orders_delivered,
                    placed_accepted_score = EXCLUDED.placed_accepted_score,
                    accepted_prepared_score = EXCLUDED.accepted_prepared_score,
                    prepared_delivered_score = EXCLUDED.prepared_delivered_score,
                    avg_rating_score = EXCLUDED.avg_rating_score,
                    percentage_order_fulfilled_score = EXCLUDED.percentage_order_fulfilled_score,
                    score = EXCLUDED.score
            """
            k = (str(df["rid"][row]),str(df["rid"][row]), int(df["No-of_orders_delivered"][row]), float(df["PLACED-ACCEPTED-AVG-SCORE"][row]), float(df["ACCEPTED-PREPARED-AVG-SCORE"][row]), float(df["PREPARED-DELIVERED-AVG-SCORE"][row]), float(df["restaurant_avg_rating-score"][row]), float(df["PercentageOrderFulfilled-score"][row]), float(df["score"][row]))

            con.execute(query,k)  

        query="""UPDATE gintaa_food_listing.restaurant_health_index
            SET score = 0
            WHERE rid IN ({})""".format(", ".join(["%s"] * len(blacklisted_rids)))
        con.execute(query,blacklisted_rids['rid'].to_list())

        conn.commit()  
            
                
        message= "Write to DB done"
        return message