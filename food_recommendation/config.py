import os


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
        return sql_connection
    
    @staticmethod
    def food_listing_sql_config():

        sql_connection= {

            "database" :os.environ['FOOD_LISTING_POSTGRESQL_DATABASE'],
            "user": os.environ['FOOD_LISTING_POSTGRESQL_USERNAME'],
            "password":os.environ['FOOD_LISTING_POSTGRESQL_PASSWORD'],
            "host":os.environ['FOOD_LISTING_POSTGRESQL_HOST'],
            "port":os.environ['FOOD_LISTING_POSTGRESQL_PORT']
        }
        return sql_connection
    
    @staticmethod
    def no_of_days():

        no_of_days = int(os.environ['GINTAA_NUMBER_OF_DAYS'])
        user_no_of_days = int(os.environ['GINTAA_USER_NUMBER_OF_DAYS'])
        return no_of_days, user_no_of_days