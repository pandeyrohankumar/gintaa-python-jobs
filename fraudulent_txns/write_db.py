import psycopg2
from config import CONN_PATH
class INSERT_TO_DB():
    def write_to_db(self,df):
        sql_connect=CONN_PATH().stats_sql_config_deals()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        con = conn.cursor()
        con.execute("TRUNCATE TABLE gintaa_deals.fraudulent_transaction")

        for row in df.index:
            query = "INSERT INTO gintaa_deals.fraudulent_transaction(id,ref_id,reason) VALUES (%s,%s,%s)"
            k=(str(row+1),str(df["deal_ref_id"][row]),str(df["reason"][row]))
            print(k)
            con.execute(query,k)
                
        conn.commit()             
        message= "Write to DB done"

        return message