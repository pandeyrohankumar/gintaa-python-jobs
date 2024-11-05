import os
from google.cloud import bigquery
from google.oauth2 import service_account
import json


class CONN_PATH:

    @staticmethod
    def big_query_conn():
        service_account_info=json.loads(os.environ['BIG_QUERY_KEY'])
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id = os.environ['PROJECT_ID']
        client = bigquery.Client(credentials= credentials,project=project_id)
        time_period = int(os.environ['TIME_PERIOD'])
        return client, project_id, time_period
    