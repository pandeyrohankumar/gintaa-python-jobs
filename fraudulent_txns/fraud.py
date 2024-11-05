from config import CONN_PATH
import psycopg2
import pandas as pd

class FRAUD():
    def fraud_transaction(self):
        sql_connect=CONN_PATH().stats_sql_config_deals()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)

        deal_closed_table=pd.read_sql(("SELECT dst.deal_ref_id,dst.created_date FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('CLOSED') and dst.deal_ref_id is not null"), conn)
        deal_partial_closed_table=pd.read_sql(("SELECT dst.deal_ref_id,dst.created_date FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('PARTIAL_CLOSED') and dst.deal_ref_id is not null"), conn)        
        deal_initiate_table=pd.read_sql(("SELECT dst.deal_ref_id,dst.created_date FROM gintaa_deals.deal_state_transition_log dst,gintaa_deals.deal_status_master dm where dm.id = dst.deal_status_code and dm.deal_status_code IN ('INITIATED') and dst.deal_ref_id is not null"), conn)
        deal_closed_df=pd.DataFrame(data=deal_closed_table,index=None)
        deal_partial_closed_df=pd.DataFrame(data=deal_partial_closed_table,index=None)
        deal_initiate_df=pd.DataFrame(data=deal_initiate_table,index=None)

        merged_df = pd.merge(deal_closed_df, deal_partial_closed_df, on='deal_ref_id', how='inner')
        deal_partial_closed_df = deal_partial_closed_df[~deal_partial_closed_df['deal_ref_id'].isin(merged_df['deal_ref_id'])]

        deal_closed_df_time=pd.merge(deal_closed_df,deal_initiate_df , on='deal_ref_id', how='left')
        deal_closed_df_time['Time']=(deal_closed_df_time["created_date_x"]-deal_closed_df_time["created_date_y"]).dt.total_seconds() / 60

        #Drop deals which transaction time is more than 150 min
        deal_closed_df_time.drop(deal_closed_df_time[deal_closed_df_time["Time"]>150 ].index, inplace = True)
        lst=list(set(deal_closed_df_time['deal_ref_id'].tolist()))
        closed_df= pd.DataFrame(lst,columns=['deal_ref_id'])
        closed_df['reason']='Closed transaction time is less than 150 min'


        deal_partial_closed_df_time=pd.merge(deal_partial_closed_df,deal_initiate_df , on='deal_ref_id', how='left')
        deal_partial_closed_df_time['Time']=(deal_partial_closed_df_time["created_date_x"]-deal_partial_closed_df_time["created_date_y"]).dt.total_seconds() / 60

        #Drop deals which transaction time is more than 100 min
        deal_partial_closed_df_time.drop(deal_partial_closed_df_time[deal_partial_closed_df_time["Time"]>100 ].index, inplace = True)
        lst=list(set(deal_partial_closed_df_time['deal_ref_id'].tolist()))
        partial_closed_df= pd.DataFrame(lst,columns=['deal_ref_id'])
        partial_closed_df['reason']='Partial closed transaction time of deal which has not been closed is less than 100 min'

        df = pd.concat([closed_df, partial_closed_df], ignore_index=True)

        return df
    