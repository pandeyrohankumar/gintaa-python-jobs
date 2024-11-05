

class CONN_PATH():
    def init_config(self):

        connection= {
            "database" :"statistics",
            "user":"einstein",
            "password":"Hagintaa12357",
            "host":"35.240.161.143",
            "port":5432
        }

        # connection = {
        #     "database" : "statistics",
        #     "user": os.environ['STATISTICS_DB_USER'],
        #     "password": os.environ['STATISTICS_DB_PASSWORD'],
        #     "host": os.environ['STATISTICS_DB_HOST'],
        #     "port":5432
        # }
        return connection

    def elastic_config(self):
        connection={
            "host" :"localhost",
            "port":9200,
            "user":"elastic",
            "password":"H44xXxax-fMdhZgv3LyV"

        }
        # connection={
        #     "host" :os.environ['ELASTIC_HOST'],       
        #     "port":9200,
        #     "user":os.environ['ELASTIC_USER'],
        #     "password":os.environ['ELASTIC_USER_PASSWORD']

        # }

        return connection





    


#  psycopg2.connect(database="postgres", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")