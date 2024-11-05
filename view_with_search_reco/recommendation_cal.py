import pandas as pd
from config import CONN_PATH
import psycopg2
from datetime import datetime, timedelta


class RECOMMENDATION_CAL():
  def reco(self):
    time_period=CONN_PATH().time_period()
    last_run_time = datetime.now() - timedelta(hours = int(time_period))
    last_run_time=last_run_time.strftime('%Y-%m-%d %H:%M:%S')
    client,bq_events_table_name=CONN_PATH().big_query_conn()
    query_job1 = client.query(f"""
    SELECT user_id,ep.value.string_value as oid,event_date,FORMAT_TIME('%T', TIME(TIMESTAMP_MICROS(event_timestamp),'Asia/Kolkata'))event_time FROM `{bq_events_table_name}.events_intraday_*`,unnest (event_params) ep  where event_name="gintaa_product_details" and ep.key="listing_id" and user_id IS NOT NULL  """)

    bq_view_df = query_job1.result().to_dataframe()
    bq_view_df["event_datetime"]=""
    for i in bq_view_df.index:
        date=bq_view_df["event_date"][i]
        bq_view_df["event_date"][i]=date[:4]+"/"+date[4:6]+"/"+date[6:]
        bq_view_df["event_datetime"][i]=datetime.strptime(bq_view_df["event_date"][i]+" "+bq_view_df["event_time"][i],'%Y/%m/%d %H:%M:%S')
    

    bq_view_df["event_datetime"]=pd.to_datetime(bq_view_df["event_datetime"])
    bq_view_df.drop(bq_view_df[bq_view_df["event_datetime"] < last_run_time ].index, inplace = True)

    query_job2 = client.query(f"""
      SELECT user_id,ep.value.string_value as query_text ,event_date,FORMAT_TIME('%T', TIME(TIMESTAMP_MICROS(event_timestamp),'Asia/Kolkata'))event_time,count(1) as query_count FROM `{bq_events_table_name}.events_intraday_*`,unnest (event_params) ep  where event_name="gintaa_search_query" and ep.key= "query_text" and user_id IS NOT NULL group by 1,2,3,4""")

    bq_search_df_all = query_job2.result().to_dataframe()
    bq_search_df_all["event_datetime"]=""
    for i in bq_search_df_all.index:
        date=bq_search_df_all["event_date"][i]
        bq_search_df_all["event_date"][i]=date[:4]+"/"+date[4:6]+"/"+date[6:]
        bq_search_df_all["event_datetime"][i]=datetime.strptime(bq_search_df_all["event_date"][i]+" "+bq_search_df_all["event_time"][i],'%Y/%m/%d %H:%M:%S')
    

    bq_search_df_all["event_datetime"]=pd.to_datetime(bq_search_df_all["event_datetime"])
    bq_search_df_all.drop(bq_search_df_all[bq_search_df_all["event_datetime"] < last_run_time ].index, inplace = True)


    bq_search_df=bq_search_df_all[['user_id']]
  
    sql_connect=CONN_PATH().stats_sql_config()
    conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
    print("=====ESTABLISHING CONNECTION, DETAILS=====")
    print(conn)
    listing_table = pd.read_sql(("SELECT oid,identity_id,category_id,category FROM gintaa_statistics.offer_statistics;"), conn)

    listing_df= pd.DataFrame(data=listing_table,index=None)
    # listing_df=pd.read_excel("gintaa_statistics_data_03-01-2023.xlsx")
    
    top_listing_table=pd.read_sql("SELECT listing_date, category_id,oid,score,rn FROM (SELECT DATE(created_date) as listing_date,category_id,oid,score,offer_stage, ROW_NUMBER() OVER(PARTITION BY category_id ORDER BY score DESC)as rn FROM gintaa_statistics.offer_statistics where offer_stage='Published')RNK where rn<=10 ",conn)
    top_listing_df=pd.DataFrame(data=top_listing_table,index=None)
    # top_listing_df=pd.read_excel("Category Id bassed on listing score 10-01-2023.xlsx")
    top_listing_group=top_listing_df.groupby('category_id')['oid'].apply(list)
    top_listing_df=top_listing_group.to_frame().reset_index()
    for i in top_listing_df.index:
      top_listing_df['oid'][i]=str(top_listing_df['oid'][i]).replace("[",'').replace("]",'').replace("'",'')


    view_df=pd.merge(bq_view_df,listing_df , on='oid', how='left')

    #Line 15-20 commented to fetch search user_id and line 44 to get only search with view
    view_df=pd.merge(bq_search_df ,view_df, on='user_id', how='left')
    view_df = view_df[view_df['user_id'] != view_df['identity_id']]
    view_df.drop(['oid', 'identity_id'], axis=1)
    view_df=view_df.groupby(['user_id', 'category_id','category']).size()
    view_final_df=view_df.to_frame().reset_index()
    view_final_df.rename(columns = {0:'count'}, inplace = True)

    view_final_df=pd.merge(view_final_df,top_listing_df,on='category_id',how='left')

    # view_final_df.to_excel("Result(demo)_10-01-2023.xlsx",index=False)
    return view_final_df





