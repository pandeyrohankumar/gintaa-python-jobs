import psycopg2
from config import CONN_PATH
class INSERT_TO_DB():
        def write_to_db(self,df):
            sql_connect=CONN_PATH().stats_sql_config()
            conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])


            con = conn.cursor()
            
            con.execute("TRUNCATE TABLE gintaa_statistics.search_reco")
            for row in df.index:

                query = "INSERT INTO gintaa_statistics.search_reco (user_id,category_id,category,count,oid) VALUES (%s,%s,%s,%s,%s)"
                k=(str(df["user_id"][row]),str(df["category_id"][row]),str(df["category"][row]),str(df["count"][row]),str(df["oid"][row]))
                print(k)
                con.execute(query,k)  

            conn.commit()  
            
                
            message= "Write to DB done"
            return message