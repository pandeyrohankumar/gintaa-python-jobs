import psycopg2
from config import CONN_PATH
class WRITE_IN_DB():
    def update_db(self,df):
        sql_connect=CONN_PATH().stats_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])


        con = conn.cursor()
        
        for row in df.index:

            sql = "UPDATE gintaa_statistics.user_stat_table SET seller_score = %s WHERE uid = %s"
            k=(str(df["score"][row]),str(df["receiving_user_id"][row]))
            con.execute(sql,k)  

        conn.commit()

        return "Done"