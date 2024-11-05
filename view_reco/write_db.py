import psycopg2
from config import CONN_PATH
class INSERT_TO_DB():
        def write_to_db(self,df):
            sql_connect=CONN_PATH().stats_sql_config()
            conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
            con = conn.cursor()
            
            for row in df.index:

                query = "INSERT INTO gintaa_statistics.view_reco (user_id,category_id,category,count) VALUES (%s,%s,%s,%s)"
                k=(str(df["user_id"][row]),str(df["category_id"][row]),str(df["category"][row]),float(df["count"][row]))
                print(k)
                con.execute(query,k)  

            conn.commit()  
                 
            message= "Write to DB done"
            return message

        def update_db(self,df,df2):
            sql_connect=CONN_PATH().stats_sql_config()
            conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
            con = conn.cursor()
            
            # set_user_id=tuple(set(df["user_id"]))

            # query = f"DELETE FROM gintaa_statistics.view_reco WHERE user_id IN {set_user_id}"
            # con.execute(query)
            for row in df.index:

                query = "INSERT INTO gintaa_statistics.view_reco (user_id,category_id,category,count) VALUES (%s,%s,%s,%s)"
                k=(str(df["user_id"][row]),str(df["category_id"][row]),str(df["category"][row]),float(df["count"][row]))
                print(k)
                con.execute(query,k)  

            conn.commit()     

            for row in df2.index:

                query = "UPDATE gintaa_statistics.view_reco SET count=%s WHERE user_id=%s AND category_id=%s AND category=%s "
                k=((float(df2["count"][row])),str(df2["user_id"][row]),str(df2["category_id"][row]),str(df2["category"][row]))
                print(k)
                con.execute(query,k)  

            conn.commit()              
                
            message= "Write to DB done"
            return message