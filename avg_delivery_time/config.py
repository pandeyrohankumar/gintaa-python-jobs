import os
import urllib.parse

class ConnPath():    

    @staticmethod
    def food_order_sql_config():

        sql_connection= {

            "database" :os.environ['FOOD_ORDER_POSTGRESQL_DATABASE'],
            "user": os.environ['FOOD_ORDER_POSTGRESQL_USERNAME'],
            "password":os.environ['FOOD_ORDER_POSTGRESQL_PASSWORD'],
            "host":os.environ['FOOD_ORDER_POSTGRESQL_HOST'],
            "port":os.environ['FOOD_ORDER_POSTGRESQL_PORT']
        }
        no_of_days = int(os.environ['GINTAA_NUMBER_OF_DAYS'])
        return sql_connection, no_of_days
    
    @staticmethod
    def offers_mongo_config():
        mongo_connection = {

            "host": os.environ['MONGO_HOST'],
            "port": os.environ['MONGO_PORT'],
            "user": os.environ['MONGO_USER'],
            "password": os.environ['MONGO_PASSWORD'],
            "database": os.environ['MONGO_DATABASE']
        }
        return mongo_connection

    @staticmethod
    def offers_mongo_conn_str():
        mongo_connection = ConnPath.offers_mongo_config()
        if os.environ['PROFILE'] == 'dev':
            return f'mongodb://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}:{mongo_connection["port"]}/{mongo_connection["database"]}', mongo_connection["database"]
        return f'mongodb+srv://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}/{mongo_connection["database"]}', mongo_connection["database"]