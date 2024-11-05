import psycopg2
from config import CONN_PATH
class INSERT_TO_DB():
        def write_to_db(self,df):
            sql_connect=CONN_PATH().stats_sql_config()
            conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
            con = conn.cursor()
            con.execute("TRUNCATE TABLE gintaa_statistics.popularity_score")

            for row in df.index:
                query = "INSERT INTO gintaa_statistics.popularity_score(oid,popularity_score) VALUES (%s,%s)"
                k=(str(df["oid"][row]),float(df["popularity_score"][row]))
                con.execute(query,k)
                  
            conn.commit()             
            message= "Write to DB done"

            return message