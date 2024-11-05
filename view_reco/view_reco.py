import pandas as pd
from config import CONN_PATH
import psycopg2
import numpy as np
from datetime import datetime, timedelta


class VIEW_RECO():
    def view_reco_overall(self):

        client,bq_table_name=CONN_PATH().big_query_conn()
        query_job1 = client.query(f"""
        SELECT user_id,ep.value.string_value as oid FROM `{bq_table_name}.events_*`,unnest (event_params) ep  where event_name="gintaa_product_details" and ep.key="listing_id" and user_id IS NOT NULL  """)


        bq_view_df = query_job1.result().to_dataframe()
        print(bq_view_df)
        # bq_view_df = pd.read_excel("view.xlsx")

        sql_connect=CONN_PATH().stats_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)
        listing_table = pd.read_sql(("SELECT oid,identity_id,category_id,category FROM gintaa_statistics.offer_statistics;"), conn)

        listing_df= pd.DataFrame(data=listing_table,index=None)
        # print(listing_df)

        df=pd.merge(bq_view_df,listing_df , on='oid', how='left')
        df = df[df['user_id'] != df['identity_id']]
        print(df)
        df.drop(['oid', 'identity_id'], axis=1)
        final_df=df.groupby(['user_id', 'category_id','category']).size()
        final_df=final_df.to_frame().reset_index()
        final_df=final_df.rename(columns={0: 'count'})
        print(final_df)
        # final_df.to_excel("Result(Overall).xlsx")
        return final_df

    def view_reco_intraday(self):
        time_period=CONN_PATH().time_period()
        last_run_time = datetime.now() - timedelta(hours = int(time_period))
        last_run_time=last_run_time.strftime('%Y-%m-%d %H:%M:%S')
        client,bq_table_name=CONN_PATH().big_query_conn()
        query_job1 = client.query(f"""
        SELECT user_id,ep.value.string_value as oid,event_date,FORMAT_TIME('%T', TIME(TIMESTAMP_MICROS(event_timestamp),'Asia/Kolkata'))event_time FROM `{bq_table_name}.events_intraday_*`,unnest (event_params) ep  where event_name="gintaa_product_details" and ep.key="listing_id" and user_id IS NOT NULL  """)

        bq_view_df = query_job1.result().to_dataframe()
        bq_view_df["event_datetime"]=""
        for i in bq_view_df.index:
            date=bq_view_df["event_date"][i]
            bq_view_df["event_date"][i]=date[:4]+"/"+date[4:6]+"/"+date[6:]
            bq_view_df["event_datetime"][i]=datetime.strptime(bq_view_df["event_date"][i]+" "+bq_view_df["event_time"][i],'%Y/%m/%d %H:%M:%S')
        

        bq_view_df["event_datetime"]=pd.to_datetime(bq_view_df["event_datetime"])
        bq_view_df.drop(bq_view_df[bq_view_df["event_datetime"] < last_run_time ].index, inplace = True)

        print(bq_view_df)
        # bq_view_df = pd.read_excel("view.xlsx")

        sql_connect=CONN_PATH().stats_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)
        listing_table = pd.read_sql(("SELECT oid,identity_id,category_id,category FROM gintaa_statistics.offer_statistics;"), conn)

        listing_df= pd.DataFrame(data=listing_table,index=None)
        # print(listing_df)

        df=pd.merge(bq_view_df,listing_df , on='oid', how='left')
        df = df[df['user_id'] != df['identity_id']]
        print(df)
        df.drop(['oid', 'identity_id'], axis=1)
        final_df=df.groupby(['user_id', 'category_id','category']).size()
        final_df=final_df.to_frame().reset_index()
        final_df=final_df.rename(columns={0: 'count'})
        print(final_df)

        view_reco_table=pd.read_sql("SELECT * FROM gintaa_statistics.view_reco", conn)
        view_reco_df=pd.DataFrame(data=view_reco_table,index=None)
        final_df['count']=final_df['count'].astype(np.float64)
        # print(final_df.dtypes)
        view_reco_df['count']=view_reco_df['count'].astype(np.float64)
        # print(view_reco_df.dtypes)
        
        # df_to_update = final_df.merge(view_reco_df, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1)
        merge_df = final_df.merge(view_reco_df.drop_duplicates(), on=['user_id','category_id','category'],how='left', indicator=True)
        
        df_to_write=merge_df[merge_df['_merge'] == 'left_only']
        df_to_write.drop(['count_y', '_merge'], axis=1)
        df_to_write.rename(columns = {'count_x':'count'}, inplace = True)

        df_to_both=merge_df[merge_df['_merge'] == 'both']
        df_to_both["count"]=df_to_both["count_x"]+df_to_both["count_y"]

        print(df_to_both)
        print(df_to_write)
        # print(df_to_update)
        # final_df.to_excel("Result1(Intraday).xlsx")
        return df_to_write,df_to_both

