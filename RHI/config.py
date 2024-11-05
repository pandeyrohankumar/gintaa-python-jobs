import os
from google.cloud import bigquery
from google.oauth2 import service_account
import json

class CONN_PATH():

    def food_order_sql_config(self):

        sql_connection= {

            "database" :os.environ['FOOD_ORDER_POSTGRESQL_DATABASE'],
            "user": os.environ['FOOD_ORDER_POSTGRESQL_USERNAME'],
            "password":os.environ['FOOD_ORDER_POSTGRESQL_PASSWORD'],
            "host":os.environ['FOOD_ORDER_POSTGRESQL_HOST'],
            "port":os.environ['FOOD_ORDER_POSTGRESQL_PORT']
        }
        return sql_connection
    
    def food_listing_sql_config(self):

        sql_connection= {

            "database" :os.environ['FOOD_LISTING_POSTGRESQL_DATABASE'],
            "user": os.environ['FOOD_LISTING_POSTGRESQL_USERNAME'],
            "password":os.environ['FOOD_LISTING_POSTGRESQL_PASSWORD'],
            "host":os.environ['FOOD_LISTING_POSTGRESQL_HOST'],
            "port":os.environ['FOOD_LISTING_POSTGRESQL_PORT']
        }
        return sql_connection

    def big_query_conn(self):

        service_account_info=json.loads(os.environ["BIG_QUERY_KEY"])
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id = os.environ['PROJECT_ID']
        client = bigquery.Client(credentials= credentials,project=project_id)
        bq_table_name=os.environ['BIGQUERY_RHI_TABLE_NAME']

        return client,bq_table_name
    
    def time_period(self):
        time_period=os.environ['TIME_PERIOD']
        return time_period