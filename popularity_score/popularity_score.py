import pandas as pd
from datetime import datetime,date
from config import CONN_PATH
import psycopg2

class POPULARITY_SCORE():
    def premium_listing(self):
        sql_connect=CONN_PATH().subs_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)
        premium_table=pd.read_sql(("SELECT offer_id as oid FROM gintaa_subscription.featured_listing;"), conn)
        premium_df=pd.DataFrame(data=premium_table,index=None)
        return premium_df


    def listing_score_view(self):
        sql_connect=CONN_PATH().stats_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        print(conn)
        listing_score_table = pd.read_sql(("SELECT DATE(created_date) AS date,oid,view_count,score FROM gintaa_statistics.offer_statistics where offer_stage='Published' and score is not NULL;"), conn)
        listing_score_df= pd.DataFrame(data=listing_score_table,index=None)
        return listing_score_df
    

    def generate_score(self):
        df=POPULARITY_SCORE().listing_score_view()
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')


        # Get today's date
        today = pd.Timestamp(date.today())

        # Calculate the number of days from today for each date
        df['No of days'] = today - df['date']
        df['No of days'] = df['No of days'].fillna(pd.Timedelta(0))
        df['No of days'] = df['No of days'].dt.days.astype(int)
        

        df['avg_view_count']=''
        for i in df.index:
            if df['No of days'][i]==0:
                df['avg_view_count'][i]=df['view_count'][i]
            else:
                df['avg_view_count'][i]=df['view_count'][i]/df['No of days'][i]

        premium_df=POPULARITY_SCORE().premium_listing()
        premium_oids = premium_df['oid']
        # print(premium_oids)

        premium_oid_set = set(premium_oids)
        df['premium'] = df['oid'].apply(lambda x: 1 if x in premium_oid_set else 0)
        # print(df)

        max_view_count=df["avg_view_count"].max()
        df["popularity_score"]=((df["avg_view_count"]/max_view_count)*50/100)+(df["score"]*42/100)
        for i in df.index:
            if df['premium'][i]==1:
                df["popularity_score"][i]+=8
        df = df.filter(['oid', 'popularity_score'])
        return df
