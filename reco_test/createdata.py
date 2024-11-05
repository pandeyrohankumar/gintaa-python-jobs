import pandas as pd
from config import CONN_PATH
import urllib.parse
from pymongo import MongoClient
import random

class CREATEDATA():
    def createdata(self):
        client,bq_table_name=CONN_PATH().big_query_conn()
        query_job1 = client.query("""
        SELECT user_id,count(1) FROM `%s.events_*`,unnest (event_params) ep  where event_name="gintaa_product_details"  and user_id IS NOT NULL group by 1 """%bq_table_name)

        df = query_job1.result().to_dataframe()
        df = df.reindex(df.index.repeat(3)).reset_index(drop=True)
        print(df)
        mongo_connection=CONN_PATH().offers_mongo_config()
        client = MongoClient(f'mongodb://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}:{mongo_connection["port"]}/{mongo_connection["database"]}') 
        oid_df = client.offers.published_offer.find({"offerStage":"Published"},{ "oid" :1})
        oid=[]
        category=['Book','Mobile','Laptop','Bike']
        category_id=['2iebdfRzKKSsdnewVtZJNZ','2Jmis6IRy2rdnsPURg0yeL','4c14DkZtDSGplOB5dPyZfq']
        df['category']=''
        df['category_id']=''
        df['count']=''
        df["oid"]=''
        for i in oid_df:
            oid.append(i["oid"])
        for i in df.index:
            li=[]
            for k in range(1,4):
                li.append(random.choice(oid))
            new_variable = ", ".join(li)
            df["oid"][i]=new_variable
            df['category'][i]=random.choice(category)
            df['category_id'][i]=random.choice(category_id)
            df['count'][i]=i+2
        return df