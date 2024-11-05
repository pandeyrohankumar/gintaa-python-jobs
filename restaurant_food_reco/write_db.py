import psycopg2
from config import CONN_PATH
class WRITE_DB():
    def write_to_db(self,df):
        sql_connect=CONN_PATH().food_listing_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])


        con = conn.cursor()
        
        con.execute("TRUNCATE TABLE gintaa_food_listing.restaurant_food_recommendation")
        for row in df.index:

            query = "INSERT INTO gintaa_food_listing.restaurant_food_recommendation (rid,food_listing_id,score,type) VALUES (%s,%s,%s,%s)"
            k=(str(df["rid"][row]),str(df["food_listing_id"][row]),str(df["score"][row]),str(df["type"][row]))
            con.execute(query,k)  

        conn.commit()  
            
                
        message= "Write to DB done"
        return message