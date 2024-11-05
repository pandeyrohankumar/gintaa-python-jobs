import pandas as pd
from config import CONN_PATH
import psycopg2


class RESTAURANT_TOP_SELLING_FOOD():

    def restaurant_top_selling_food(self):
        sql_food_order_connect=CONN_PATH().food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_order)

        sql_food_listing_connect=CONN_PATH().food_listing_sql_config()
        conn_food_listing = psycopg2.connect(database=sql_food_listing_connect["database"], user = sql_food_listing_connect["user"], password = sql_food_listing_connect["password"], host = sql_food_listing_connect["host"], port = sql_food_listing_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn_food_listing)
        
        restaurant_top_selling_food_table=pd.read_sql(("SELECT fod.food_listing_id AS fid, fl.rid, COUNT(fod.food_listing_id) AS txns_count FROM gintaa_food_order.food_order_details AS fod INNER JOIN gintaa_food_order.food_listing AS fl ON fl.id = fod.food_listing_id INNER JOIN gintaa_food_order.food_order AS fo ON fo.id = fod.food_order_id WHERE fo.order_status = 'DELIVERED' GROUP BY fod.food_listing_id, fl.rid;"), conn_food_order)
        restaurant_top_selling_food_df=pd.DataFrame(data=restaurant_top_selling_food_table,index=None)

        active_food_listing_table=pd.read_sql("SELECT id as fid from gintaa_food_listing.food_listing where active='true'",conn_food_listing)
        active_food_listing_df=pd.DataFrame(data=active_food_listing_table,index=None)

        restaurant_top_selling_food_df=pd.merge(restaurant_top_selling_food_df,active_food_listing_df,on='fid',how='inner')

        return restaurant_top_selling_food_df