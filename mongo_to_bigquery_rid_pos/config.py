import os
import urllib.parse
from google.cloud import bigquery
from google.oauth2 import service_account
import json


class ConnPath():

    def offers_mongo_config(self):
        
        mongo_connection = {

            "host": os.environ['REATAURANT_MGMT_MONGO_HOST'],
            "port": os.environ['REATAURANT_MGMT_MONGO_PORT'],
            "user": os.environ['REATAURANT_MGMT_MONGO_USER'],
            "password": os.environ['REATAURANT_MGMT_MONGO_PASSWORD'],
            "database": os.environ['REATAURANT_MGMT_MONGO_DATABASE']
        }
        return mongo_connection
    
    def offers_mongo_conn_str(self):

        mongo_connection = self.offers_mongo_config()
        if os.environ['PROFILE'] == 'dev':
            return f'mongodb://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}:{mongo_connection["port"]}/{mongo_connection["database"]}'
        return f'mongodb+srv://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}/{mongo_connection["database"]}'

    def big_query_conn(self):

        service_account_info=json.loads(os.environ["BIG_QUERY_KEY"])
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id = os.environ['PROJECT_ID']
        client = bigquery.Client(credentials= credentials,project=project_id)
        bq_table_name=os.environ['BIGQUERY_TABLE_NAME']

        return client,bq_table_name