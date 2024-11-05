from pymongo import MongoClient
from config import ConnPath

class UpdateDeliveryTime:
    def update_delivery_time(data_to_insert):
        connection_string, database_name = ConnPath.offers_mongo_conn_str()

        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db["third_party_avg_delivery_time"]

        collection.delete_many({})

        collection.insert_many(data_to_insert)

        return "Data Updated Successfully"
