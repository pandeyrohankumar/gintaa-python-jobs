import psycopg2
from config import CONN_PATH
class INSERT_TO_DB():
        def write_to_db(self,df):
            sql_connect=CONN_PATH().stats_sql_config()
            conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])


            con = conn.cursor()
            
            con.execute("TRUNCATE TABLE gintaa_statistics.advertisement_statistics")
            for row in df.index:

                query = "INSERT INTO gintaa_statistics.advertisement_statistics (advertisement,impr_count) VALUES (%s,%s)"
                k=(str(df['string_value'][row]),str(df['impr_count'][row]))
                print(k)
                con.execute(query,k)  

            conn.commit()  
            
                
            message= "Write to DB done"
            return message