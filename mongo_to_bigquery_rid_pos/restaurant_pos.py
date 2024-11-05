import pandas as pd
from pymongo import MongoClient
from config import ConnPath

class RestaurantPos():
    def get_data(self):
        mongo_str = ConnPath().offers_mongo_conn_str()
        client = MongoClient(mongo_str)
        collection = client.restaurant_mgmt_intg.restaurant_platform_data
        
        all_data_df = collection.find({}, {"rid": 1, "platform": 1})
        
        print("=====CONNECTION DETAILS=====")
        
        rid = []
        platform = []
        
        for x in all_data_df:
            rid.append(x.get('rid', None))
            platform.append(x.get('platform', None))
        
        df = pd.DataFrame({
            "rid": rid,
            "platform": platform
        })
        
        return df
