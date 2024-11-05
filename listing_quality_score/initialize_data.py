from pymongo import MongoClient
from config import CONN_PATH
from datetime import datetime, timedelta


class INITIALIZE_DATA():
    def fetch_data(self):
        mongo_str=CONN_PATH().offers_mongo_conn_str()
        client = MongoClient(mongo_str)
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        all_data_df = client.offers.published_offer.find({"lastModifiedDate": {"$gte": three_days_ago}},{ "oid" :1, "name" : 1, "description": 1,"category" :1,"returnable":1,"cod" :1,"freeShipping" : 1,"images":1,"offerStage":1,"offerAttrs":1,"facets":1,"unitOfferValuation":1,"price":1,"videos":1})
        # print(all_data_df)
        print("=====CONNECTION DETAILS=====")
        print(client)
        return all_data_df