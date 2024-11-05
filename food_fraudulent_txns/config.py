import os


class ConnPath:

    @staticmethod
    def food_order_sql_config():
        sql_connection = {
            "database": os.environ['FOOD_ORDER_POSTGRESQL_DATABASE'],
            "user": os.environ['FOOD_ORDER_POSTGRESQL_USERNAME'],
            "password": os.environ['FOOD_ORDER_POSTGRESQL_PASSWORD'],
            "host": os.environ['FOOD_ORDER_POSTGRESQL_HOST'],
            "port": os.environ['FOOD_ORDER_POSTGRESQL_PORT']
        }
        return sql_connection

    @staticmethod
    def url_gintaa_api_key_no_of_days():
        url = os.environ['GINTAA_USER_HOST'] + "/v1/user/admin/internal/blocked-users"
        gintaa_api_key = os.environ['API_KEY']
        no_of_days = int(os.environ['GINTAA_NUMBER_OF_DAYS'])
        return url, gintaa_api_key, no_of_days
