import psycopg2
from config import ConnPath


class FetchData:

    @staticmethod
    def fetch_data():
        sql_food_order_connect, no_of_days = ConnPath().food_order_sql_config()
        pg_conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"], user = sql_food_order_connect["user"], password = sql_food_order_connect["password"], host = sql_food_order_connect["host"], port = sql_food_order_connect["port"])

        pg_cursor = pg_conn_food_order.cursor()


        sql_query = """
        WITH cte1 AS (
            SELECT
                fo1.order_id,
                EXTRACT(EPOCH FROM (fo2.created_date - fo1.created_date)) / 60 AS delivery_time
            FROM
                gintaa_food_order.food_order_status_transition_log fo1
            JOIN
                gintaa_food_order.food_order_status_transition_log fo2
                ON fo1.order_id = fo2.order_id
            WHERE
                fo1.next_state_id = 'PREPARED'
                AND fo2.next_state_id = 'DELIVERED'
                AND fo1.created_date < fo2.created_date
        ),
        cte2 AS (
            SELECT
                id,
                delivery_partner,
                distance_gmap
            FROM
                gintaa_food_order.food_order
            WHERE
                order_status = 'DELIVERED'
                AND delivery_type = 'THIRD_PARTY'
                AND created_date >= NOW() - INTERVAL '%(no_of_days)s days'
        )
        SELECT
            delivery_partner,
            AVG(delivery_time / distance_gmap) AS avg_delivery_time_per_km
        FROM
            cte1
        INNER JOIN cte2
            ON cte2.id = cte1.order_id
        GROUP BY
            delivery_partner;
        """

        pg_cursor.execute(sql_query, {'no_of_days': no_of_days})
        result = pg_cursor.fetchall()

        data_to_insert = []
        for row in result:
            delivery_partner, avg_delivery_time_per_km = row
            data_to_insert.append({
                "delivery_partner": delivery_partner,
                "avg_delivery_time_per_km": avg_delivery_time_per_km
            })

        pg_cursor.close()
        pg_conn_food_order.close()
        
        return data_to_insert