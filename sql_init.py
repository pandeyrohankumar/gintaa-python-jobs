import psycopg2
import pandas as pd

from config import CONN_PATH


####################### Opening Connection with Database ####################

class SQL_INIT():

    def sql_conn(self):
        sql_connect=CONN_PATH().init_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====CONNECTION DETAILS=====")
        print(conn)
        # Reaad from sql into a table and then into a DataFrame
        my_table    = pd.read_sql('select * from gintaa_statistics.offer_statistics_day', conn)
        offerstats_df= pd.DataFrame(data=my_table)
        if (len(offerstats_df.index) > 1 ) :
            print("=====CONNECTION SUCCESS=====")
        else :
            print("=====CONNECTION FAILED=====")
        return conn, offerstats_df
