import os
import urllib.parse

class CONN_PATH():
    def init_config(self):
        connection = {
            "database": "statistics",
            "user": os.environ['STATISTICS_DB_USER'],
            "password": os.environ['STATISTICS_DB_PASSWORD'],
            "host": os.environ['STATISTICS_DB_HOST'],
            "port": 5432
        }
        return connection

    def offers_mongo_config(self):
        mongo_connection = {

            "host": os.environ['MONGO_HOST'],
            "port": os.environ['MONGO_PORT'],
            "user": os.environ['MONGO_USER'],
            "password": os.environ['MONGO_PASSWORD'],
            "database": os.environ['MONGO_DATABASE']
        }
        return mongo_connection

    def offers_mongo_conn_str(self):
        mongo_connection = self.offers_mongo_config()
        if os.environ['PROFILE'] == 'dev':
            return f'mongodb://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}:{mongo_connection["port"]}/{mongo_connection["database"]}'
        return f'mongodb+srv://{mongo_connection["user"]}:{urllib.parse.quote_plus(mongo_connection["password"])}@{mongo_connection["host"]}/{mongo_connection["database"]}'

    def env_path(self):
        if os.environ['PROFILE'] == 'prod':
            path = 'https://api.gintaa.com'
        else:
            path = 'https://' + os.environ['PROFILE'] + '.api.gintaa.com'
        return path

#  psycopg2.connect(database="postgres", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
