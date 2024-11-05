from config import CONN_PATH
import psycopg2
import pandas as pd

class CREATE_DATASET():
    def deals(self):
        sql_connect=CONN_PATH().stats_sql_config_deals()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)
        deal_closed_table=pd.read_sql(("SELECT dst.deal_ref_id,dst.created_date FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('CLOSED')"), conn)
        deal_initiate_table=pd.read_sql(("SELECT dst.deal_ref_id,dst.created_date FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('INITIATED')"), conn)
        deal_closed_df=pd.DataFrame(data=deal_closed_table,index=None)
        deal_initiate_df=pd.DataFrame(data=deal_initiate_table,index=None)
        deal_df=pd.merge(deal_closed_df,deal_initiate_df , on='deal_ref_id', how='left')
        deal_df['Time']=(deal_df["created_date_x"]-deal_df["created_date_y"]).dt.total_seconds() / 60
        deal_df.drop(deal_df[deal_df["Time"]< 100 ].index, inplace = True)
        deal_df.rename(columns = {'deal_ref_id':'deal_id'}, inplace = True)

        lst=list(set(deal_df['deal_id'].tolist()))
        df= pd.DataFrame(lst,columns=['deal_id'])
 
        return df
    def avg_time(self):
        sql_connect=CONN_PATH().stats_sql_config_deals()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)

        #get deal df
        deal_df=CREATE_DATASET().deals()

        #get blocked listing data to remove 
        sql_stat_connect=CONN_PATH().stats_sql_config()
        conn_stat = psycopg2.connect(database=sql_stat_connect["database"], user = sql_stat_connect["user"], password = sql_stat_connect["password"], host = sql_stat_connect["host"], port = sql_stat_connect["port"])
        blocked_table=pd.read_sql(("SELECT oid as offer_id FROM gintaa_statistics.offer_statistics where offer_stage='Blocked';"),conn_stat)
        blocked_df=pd.DataFrame(data=blocked_table,index=None)


        #No of transactions
        transaction_table=pd.read_sql(("select DATE(dm.last_modified_date) AS date1,dm.ref_id as deal_id,dm.initiating_user_id, dm.receiving_user_id, dsm.deal_status_code,dod.offer_id,dod.category_id,dod.offer_owner_id from gintaa_deals.deal_offer_details dod, gintaa_deals.deal_master dm, gintaa_deals.deal_status_master dsm where dod.deal_ref_id = dm.ref_id and dm.status_code = dsm.id and dsm.deal_status_code IN ('CLOSED'); "), conn)
        transaction_df= pd.DataFrame(data=transaction_table,index=None)
        transaction_df=transaction_df[~transaction_df['offer_id'].isin(list(blocked_df['offer_id']))]
        transaction_df=pd.merge(deal_df,transaction_df , on='deal_id', how='left')
        No_of_trans=transaction_df[["receiving_user_id","deal_status_code"]]
        result_No_of_trans=pd.DataFrame(No_of_trans.groupby(["receiving_user_id"])["deal_status_code"].count())#
        result_No_of_trans.rename(columns = {'deal_status_code':'Number of Products Sold'}, inplace = True)
        # result_No_of_trans.to_excel("NoOfTransaction.xlsx")
        # print(result_No_of_trans)
        

        #Initiated to Accepted Average time

        init_to_accept_table = pd.read_sql(("SELECT dst.deal_ref_id,dm.deal_status_code,dst.created_date,dst.triggered_by_user_id FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('INITIATED','ACCEPTED')"), conn)

        init_to_accept_df= pd.DataFrame(data=init_to_accept_table,index=None)

        init_to_accept_df1=init_to_accept_df.copy(deep=True)
        init_to_accept_df2=init_to_accept_df.copy(deep=True)


        init_to_accept_df1.drop(init_to_accept_df1[init_to_accept_df1["deal_status_code"] =='ACCEPTED'].index, inplace = True)
        init_to_accept_df2.drop(init_to_accept_df2[init_to_accept_df2["deal_status_code"] =='INITIATED'].index, inplace = True)

        init_to_accept_df2.rename(columns = {'created_date':'created_date1'}, inplace = True)
        init_to_accept_df2.rename(columns = {'deal_status_code':'deal_status_code1'}, inplace = True)
        init_to_accept_df2.rename(columns = {'triggered_by_user_id':'triggered_by_user_id1'}, inplace = True)

        init_to_accept_df=pd.merge(init_to_accept_df1,init_to_accept_df2 , on='deal_ref_id', how='inner')
        init_to_accept_df["Average Time ACCEPTED from INITIATED state in Hours"]=(init_to_accept_df["created_date1"]-init_to_accept_df["created_date"]).dt.total_seconds() / 3600

        # init_to_accept_df.to_excel("test.xlsx",index=False)
        init_to_accept_avg_time=init_to_accept_df[['triggered_by_user_id1','Average Time ACCEPTED from INITIATED state in Hours']].copy()
        init_to_accept_avg_time.rename(columns = {'triggered_by_user_id1':'receiving_user_id'}, inplace = True)
        init_to_accept_result_avg_time=pd.DataFrame(init_to_accept_avg_time.groupby(['receiving_user_id']).mean())
        # init_to_accept_result_avg_time.to_excel("init_to_accept Avg time.xlsx")
        # print(init_to_accept_result_avg_time)

        merge_df=pd.merge(result_No_of_trans,init_to_accept_result_avg_time , on='receiving_user_id', how='left')


        #Accepted to Revise Average Time
        accept_to_revise_table = pd.read_sql(("SELECT dst.deal_ref_id,dm.deal_status_code,dst.created_date,dst.triggered_by_user_id FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('ACCEPTED','PARTIAL_REVISED')"), conn)

        accept_to_revise_df= pd.DataFrame(data=accept_to_revise_table,index=None)

        accept_to_revise_df1=accept_to_revise_df.copy(deep=True)
        accept_to_revise_df2=accept_to_revise_df.copy(deep=True)


        accept_to_revise_df1.drop(accept_to_revise_df1[accept_to_revise_df1["deal_status_code"] =='ACCEPTED'].index, inplace = True)
        accept_to_revise_df2.drop(accept_to_revise_df2[accept_to_revise_df2["deal_status_code"] =='REVISED'].index, inplace = True)

        accept_to_revise_df2.rename(columns = {'created_date':'created_date1'}, inplace = True)
        accept_to_revise_df2.rename(columns = {'deal_status_code':'deal_status_code1'}, inplace = True)
        accept_to_revise_df2.rename(columns = {'triggered_by_user_id':'triggered_by_user_id1'}, inplace = True)

        accept_to_revise_df=pd.merge(accept_to_revise_df1,accept_to_revise_df2 , on='deal_ref_id', how='inner')
        accept_to_revise_df["Avg Hours to ACCEPTED from REVISED state"]=(accept_to_revise_df["created_date1"]-accept_to_revise_df["created_date"]).dt.total_seconds() / 3600

        # accept_to_revise_df.to_excel("test.xlsx",index=False)
        accept_to_revise_avg_time=accept_to_revise_df[['triggered_by_user_id1','Avg Hours to ACCEPTED from REVISED state']].copy()
        accept_to_revise_avg_time.rename(columns = {'triggered_by_user_id1':'receiving_user_id'}, inplace = True)
        accept_to_revise_result_avg_time=pd.DataFrame(accept_to_revise_avg_time.groupby(['receiving_user_id']).mean())
        # accept_to_revise_result_avg_time.to_excel("accept_to_revise Avg time.xlsx")
        # print(accept_to_revise_result_avg_time)

        merge_df=pd.merge(merge_df,accept_to_revise_result_avg_time , on='receiving_user_id', how='left')



        #Accepted to Partial Closed Average Time
        accept_to_partialclose_table = pd.read_sql(("SELECT dst.deal_ref_id,dm.deal_status_code,dst.created_date,dst.triggered_by_user_id FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('ACCEPTED','PARTIAL_CLOSED')"), conn)

        accept_to_partialclose_df= pd.DataFrame(data=accept_to_partialclose_table,index=None)

        accept_to_partialclose_df1=accept_to_partialclose_df.copy(deep=True)
        accept_to_partialclose_df2=accept_to_partialclose_df.copy(deep=True)


        accept_to_partialclose_df1.drop(accept_to_partialclose_df1[accept_to_partialclose_df1["deal_status_code"] =='PARTIAL_CLOSED'].index, inplace = True)
        accept_to_partialclose_df2.drop(accept_to_partialclose_df2[accept_to_partialclose_df2["deal_status_code"] =='ACCEPTED'].index, inplace = True)

        accept_to_partialclose_df2.rename(columns = {'created_date':'created_date1'}, inplace = True)
        accept_to_partialclose_df2.rename(columns = {'deal_status_code':'deal_status_code1'}, inplace = True)
        accept_to_partialclose_df2.rename(columns = {'triggered_by_user_id':'triggered_by_user_id1'}, inplace = True)

        accept_to_partialclose_df=pd.merge(accept_to_partialclose_df1,accept_to_partialclose_df2 , on='deal_ref_id', how='inner')
        accept_to_partialclose_df["Avg Hours to PARTIAL_CLOSED from ACCEPTED state"]=(accept_to_partialclose_df["created_date1"]-accept_to_partialclose_df["created_date"]).dt.total_seconds() / 3600

        # accept_to_partialclose_df.to_excel("test.xlsx",index=False)
        accept_to_partialclose_avg_time=accept_to_partialclose_df[['triggered_by_user_id1','Avg Hours to PARTIAL_CLOSED from ACCEPTED state']].copy()
        accept_to_partialclose_avg_time.rename(columns = {'triggered_by_user_id1':'receiving_user_id'}, inplace = True)
        accept_to_partialclose_result_avg_time=pd.DataFrame(accept_to_partialclose_avg_time.groupby(['receiving_user_id']).mean())
        # accept_to_partialclose_result_avg_time.to_excel("accept_to_partialclose Avg time.xlsx")
        # print(accept_to_partialclose_result_avg_time)

        merge_df=pd.merge(merge_df,accept_to_partialclose_result_avg_time , on='receiving_user_id', how='left')


        #Partial closed to closed Average Time


        partialclose_to_close_table = pd.read_sql(("SELECT dst.deal_ref_id,dm.deal_status_code,dst.created_date,dst.triggered_by_user_id FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('PARTIAL_CLOSED','CLOSED')"), conn)

        partialclose_to_close_df= pd.DataFrame(data=partialclose_to_close_table,index=None)

        partialclose_to_close_df1=partialclose_to_close_df.copy(deep=True)
        partialclose_to_close_df2=partialclose_to_close_df.copy(deep=True)


        partialclose_to_close_df1.drop(partialclose_to_close_df1[partialclose_to_close_df1["deal_status_code"] =='CLOSED'].index, inplace = True)
        partialclose_to_close_df2.drop(partialclose_to_close_df2[partialclose_to_close_df2["deal_status_code"] =='PARTIAL_CLOSED'].index, inplace = True)

        partialclose_to_close_df2.rename(columns = {'created_date':'created_date1'}, inplace = True)
        partialclose_to_close_df2.rename(columns = {'deal_status_code':'deal_status_code1'}, inplace = True)
        partialclose_to_close_df2.rename(columns = {'triggered_by_user_id':'triggered_by_user_id1'}, inplace = True)

        partialclose_to_close_df=pd.merge(partialclose_to_close_df1,partialclose_to_close_df2 , on='deal_ref_id', how='inner')
        partialclose_to_close_df["Avg Hours to CLOSED from PARTIAL_CLOSED state"]=(partialclose_to_close_df["created_date1"]-partialclose_to_close_df["created_date"]).dt.total_seconds() / 3600

        # partialclose_to_close_df.to_excel("test.xlsx",index=False)
        partialclose_to_close_avg_time=partialclose_to_close_df[['triggered_by_user_id1','Avg Hours to CLOSED from PARTIAL_CLOSED state']].copy()
        partialclose_to_close_avg_time.rename(columns = {'triggered_by_user_id1':'receiving_user_id'}, inplace = True)
        partialclose_to_close_result_avg_time=pd.DataFrame(partialclose_to_close_avg_time.groupby(['receiving_user_id']).mean())
        # partialclose_to_close_result_avg_time.to_excel("partialclose_to_close Avg time.xlsx")
        # print(partialclose_to_close_result_avg_time)

        merge_df=pd.merge(merge_df,partialclose_to_close_result_avg_time , on='receiving_user_id', how='left')


        # merge_df.to_excel("MergedSheet.xlsx")
        return merge_df

    def rating(self):
        sql_connect=CONN_PATH().stats_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)


        #No of transactions
        rating_table=pd.read_sql(("SELECT uid as receiving_user_id,average_rating as user_rating,registration_date as reg_date FROM gintaa_statistics.user_stat_table;"), conn)
        rating_df= pd.DataFrame(data=rating_table,index=None)
        print(rating_df)
        return rating_df
