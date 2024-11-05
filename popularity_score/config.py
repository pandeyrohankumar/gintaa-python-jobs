import os


class CONN_PATH():

    def stats_sql_config(self):

        sql_connection= {

            "database" :os.environ['STAT_POSTGRESQL_DATABASE'],
            "user": os.environ['STAT_POSTGRESQL_USERNAME'],
            "password":os.environ['STAT_POSTGRESQL_PASSWORD'],
            "host":os.environ['STAT_POSTGRESQL_HOST'],
            "port":os.environ['STAT_POSTGRESQL_PORT']
        }
        return sql_connection
    
    def subs_sql_config(self):

        sql_connection= {

            "database" :os.environ['SUBS_POSTGRESQL_DATABASE'],
            "user": os.environ['SUBS_POSTGRESQL_USERNAME'],
            "password":os.environ['SUBS_POSTGRESQL_PASSWORD'],
            "host":os.environ['SUBS_POSTGRESQL_HOST'],
            "port":os.environ['SUBS_POSTGRESQL_PORT']
        }
        return sql_connection
    

