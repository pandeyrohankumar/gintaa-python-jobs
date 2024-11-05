import psycopg2
from config import CONN_PATH
class WRITE_DB():
    def write_to_db(self,df):
        sql_connect=CONN_PATH().statistics_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])

        con = conn.cursor()
        
        con.execute("TRUNCATE TABLE gintaa_statistics.restaurant_top_selling_foods")
        for row in df.index:

            query = "INSERT INTO gintaa_statistics.restaurant_top_selling_foods (fid,rid,txns_count) VALUES (%s,%s,%s)"
            k=(str(df["fid"][row]),str(df["rid"][row]),str(df["txns_count"][row]))
            con.execute(query,k)  

        conn.commit()  
                 
        message= "Write to DB done"
        return message