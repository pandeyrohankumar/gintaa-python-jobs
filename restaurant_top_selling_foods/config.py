import os

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
    
    def statistics_config(self):

        sql_connection= {
            "database" :os.environ['STAT_POSTGRESQL_DATABASE'],
            "user": os.environ['STAT_POSTGRESQL_USERNAME'],
            "password":os.environ['STAT_POSTGRESQL_PASSWORD'],
            "host":os.environ['STAT_POSTGRESQL_HOST'],
            "port":os.environ['STAT_POSTGRESQL_PORT']
        }
        return sql_connection