import os
from google.cloud import bigquery
from google.oauth2 import service_account
import json


class CONN_PATH():
    def offers_mongo_config(self):

        mongo_connection = {
            "host": os.environ['MONGO_HOST'],
            "port": os.environ['MONGO_PORT'],
            "user":os.environ['MONGO_USER'],
            "password":os.environ['MONGO_PASSWORD'],
            "database":os.environ['MONGO_DATABASE']
        }
        return mongo_connection

    def stats_sql_config(self):

        sql_connection= {

            "database" :os.environ['STAT_POSTGRESQL_DATABASE'],
            "user": os.environ['STAT_POSTGRESQL_USERNAME'],
            "password":os.environ['STAT_POSTGRESQL_PASSWORD'],
            "host":os.environ['STAT_POSTGRESQL_HOST'],
            "port":os.environ['STAT_POSTGRESQL_PORT']
        }
        return sql_connection
    
    def big_query_conn(self):

        service_account_info=json.loads(os.environ["BIG_QUERY_KEY"])
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id = os.environ['PROJECT_ID']
        client = bigquery.Client(credentials= credentials,project=project_id)
        bq_table_name=os.environ['BIGQUERY_FIREBASE_EVENTS_TABLE_NAME']

        return client,bq_table_name

    