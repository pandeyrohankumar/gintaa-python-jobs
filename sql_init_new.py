import psycopg2
import pandas as pd
import json

from config_new import CONN_PATH


####################### Opening Connection with Database ####################

class SQL_INIT():

    def sql_conn(self):
        sql_connect=CONN_PATH().init_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====CONNECTION DETAILS=====")
        print(conn)
        # Reaad from sql into a table and then into a DataFrame
        my_table    = pd.read_sql('select * from gintaa_statistics.offer_statistics_day', conn)
        my_table1=pd.read_sql('''SELECT oid ,location_summary_json,product_age FROM gintaa_statistics.offer_statistics where is_available''', conn)
        offerstats_df= pd.DataFrame(data=my_table)
        detail_df=pd.DataFrame(data=my_table1)
        detail_df["Pincode"]=''
        detail_df["lat"]=''
        detail_df["lng"]=''
        for i in range(len(detail_df)):
            x=detail_df["location_summary_json"][i]
            y = json.loads(x)
            try:
                detail_df["lat"][i]=y["lat"]
            except:
                print("none")
            try:
                detail_df["lng"][i]=y["lng"]
            except:
                print("none")
            try:
                detail_df["Pincode"][i]=y["zip"]
            except:
                print("none")
        return conn,offerstats_df,detail_df

