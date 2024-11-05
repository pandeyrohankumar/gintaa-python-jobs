import pandas as pd
from config import CONN_PATH
import psycopg2


class RESTAURANT_FOOD_RECO():

    
    def restaurant_food_reco(self):
        sql_food_order_connect=CONN_PATH().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        sql_food_listing_connect=CONN_PATH().food_listing_sql_config()
        conn_food_listing = psycopg2.connect(database=sql_food_listing_connect["database"], user = sql_food_listing_connect["user"], password = sql_food_listing_connect["password"], host = sql_food_listing_connect["host"], port = sql_food_listing_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_listing)

        no_of_food=CONN_PATH().no_of_food()

        food_id_table=pd.read_sql(("SELECT food_order_id,food_listing_id FROM gintaa_food_order.food_order_details"), conn_food_order)
        food_id_df=pd.DataFrame(data=food_id_table,index=None)

        food_listing_txns = food_id_df['food_listing_id'].value_counts().reset_index()
        food_listing_txns.columns = ['food_listing_id', 'txns_count']
   
        food_listing_table=pd.read_sql(("SELECT id as food_listing_id,avg_rating, rid,image_url,description FROM gintaa_food_listing.food_listing "), conn_food_listing)
        food_listing_df=pd.DataFrame(data=food_listing_table,index=None)

        food_listing_df['avg_rating']=food_listing_df['avg_rating'].fillna(0)

        food_listing_df=pd.merge(food_listing_df, food_listing_txns, on='food_listing_id')

        mustTry_food_df=food_listing_df.groupby('rid').apply(lambda x: x.nlargest(int(no_of_food), 'avg_rating')).reset_index(drop=True)

        mustTry_food_df = mustTry_food_df.drop(mustTry_food_df[mustTry_food_df['avg_rating'] < 3.5].index)
        mustTry_food_df['score']=mustTry_food_df['avg_rating']

        food_listing_df = food_listing_df[~food_listing_df['food_listing_id'].isin(mustTry_food_df['food_listing_id'])]

        for i in mustTry_food_df.index:
            if pd.notna(mustTry_food_df.loc[i, 'image_url']):
                mustTry_food_df.loc[i, 'score'] += 1
            if pd.notna(mustTry_food_df.loc[i, 'description']):
                mustTry_food_df.loc[i, 'score']+=1

        bestSelling_food_df=food_listing_df.groupby('rid').apply(lambda x: x.nlargest(int(no_of_food), 'txns_count')).reset_index(drop=True)
        
        bestSelling_food_df['score']=bestSelling_food_df['txns_count']
        for i in bestSelling_food_df.index:
            if pd.notna(bestSelling_food_df.loc[i, 'image_url']):
                bestSelling_food_df.loc[i, 'score'] += 1
            if pd.notna(bestSelling_food_df.loc[i, 'description']):
                bestSelling_food_df.loc[i, 'score']+=1

        mustTry_food_df['type'] = 'must_try'
        bestSelling_food_df['type'] = 'bestseller'

        mustTry_selected = mustTry_food_df[['rid', 'food_listing_id', 'score', 'type']]
        bestSelling_selected = bestSelling_food_df[['rid', 'food_listing_id', 'score', 'type']]

        result_df = pd.concat([mustTry_selected, bestSelling_selected], ignore_index=True)

        return result_df