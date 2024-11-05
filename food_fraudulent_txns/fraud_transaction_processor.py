import pandas as pd
from config import ConnPath
import psycopg2
import requests


class FraudTransactionProcessor:

    @staticmethod
    def get_blocked_user_list(url, gintaa_api_key):
        headers = {
            "gintaa-api-key": gintaa_api_key
        }

        response = requests.get(url, headers=headers)

        # Check the status code to see if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the list of 'uid' values
            uid_list = [item['uid'] for item in response.json().get('payload', [])]

            return uid_list
            # print(uid_list)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return []

    @staticmethod
    def fetch_fraud_write_db():

        url, gintaa_api_key, no_of_days = ConnPath.url_gintaa_api_key_no_of_days()

        # no_of_days = max(1, min(no_of_days, 30))

        blocked_uid_list = FraudTransactionProcessor.get_blocked_user_list(url, gintaa_api_key)
        # return at least 1 value - user id not exists
        blocked_uid_list = blocked_uid_list if len(blocked_uid_list) > 0 else ["1"]

        sql_food_order_connect = ConnPath.food_order_sql_config()
        conn_food_order = psycopg2.connect(database=sql_food_order_connect["database"],
                                           user=sql_food_order_connect["user"],
                                           password=sql_food_order_connect["password"],
                                           host=sql_food_order_connect["host"], port=sql_food_order_connect["port"])
        print("=====ESTABLISHING CONNECTION, DETAILS=====")
        
        # Create a cursor
        cursor = conn_food_order.cursor()

        cursor.execute("TRUNCATE TABLE gintaa_food_order.fraudulent_transactions;")

        sql_query = '''
            WITH trans AS (
            SELECT 
                fo.order_id, 
                fo.uid, 
                fo.rid,
                fo.delivery_type, 
                r.name AS restaurant_name, 
                fo.user_name AS user_name,
                DATE(fo.created_date) AS created_date,
                (r.location->>'lat')::float AS r_lat,
                (r.location->>'lng')::float AS r_lng,
                (fo.delivery_address->>'lat')::float AS d_lat,
                (fo.delivery_address->>'lng')::float AS d_lng,
                6371 * acos(
                    cos(radians((fo.delivery_address->>'lat')::float)) * 
                    cos(radians((r.location->>'lat')::float)) * 
                    cos(radians((r.location->>'lng')::float) - 
                    radians((fo.delivery_address->>'lng')::float)) + 
                    sin(radians((fo.delivery_address->>'lat')::float)) * 
                    sin(radians((r.location->>'lat')::float))
                ) * 1000 AS distance_m 
            FROM 
                gintaa_food_order.food_order fo 
            LEFT JOIN 
                gintaa_food_order.restaurant r ON r.rid = fo.rid 
            WHERE 
                fo.created_date >= CURRENT_DATE - INTERVAL '%(no_of_days)s days'  
                AND (fo.gintaa_discount_value IS NOT NULL OR fo.gintaa_discount_value IS NOT NULL)
                AND fo.order_status = 'DELIVERED'
                AND uid not in %(uid_list)s
        ),
        daily_counts AS (
            SELECT
                uid,
                rid,
                restaurant_name,
                created_date,
                COUNT(*) AS day_count
            FROM trans
            GROUP BY uid, rid, restaurant_name, created_date
        ),
        aggregated_daily_counts AS (
            SELECT
                uid,
                ARRAY_AGG(json_build_object('rid', rid, 'restaurant_name', restaurant_name, 'date', created_date, 'count', day_count)) AS rid_and_day_wise_count
            FROM daily_counts
            GROUP BY uid
        ),
        daily_counts_all_rid AS (
            SELECT
                uid,
                created_date,
                COUNT(*) AS day_count_all_rid
            FROM trans
            GROUP BY uid, created_date
        ),
        aggregated_daily_counts_all_rids AS (
            SELECT
                uid,
                ARRAY_AGG(json_build_object('date', created_date, 'count', day_count_all_rid)) AS day_wise_total_count
            FROM daily_counts_all_rid
            GROUP BY uid
        ),
        order_distances AS (
            SELECT
                uid,
                ARRAY_AGG(json_build_object('order_id', order_id, 'rid', rid, 'restaurant_name', restaurant_name, 'date', created_date, 'distance', distance_m)) AS order_id_distance
            FROM trans
            WHERE delivery_type='SELF'
            GROUP BY uid
        ),
        total_counts AS (
            SELECT
                uid,
                COUNT(*) AS total_count
            FROM trans
            GROUP BY uid
        ),
        result_with_reason AS (
            SELECT
                t.uid,
                t.user_name,
                adc.rid_and_day_wise_count,
                adc_all_rid.day_wise_total_count,
                od.order_id_distance,
                tc.total_count,
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM daily_counts dc
                        WHERE dc.day_count > 1
                            AND dc.uid = t.uid
                    ) THEN 'More than 1 transaction with gintaa discount in a day for a restaurant (' || t.rid || ')'
                    WHEN EXISTS (
                        SELECT 1
                        FROM daily_counts_all_rid dcar
                        WHERE dcar.day_count_all_rid > 2
                            AND dcar.uid = t.uid
                    ) THEN 'More than 2 transactions with gintaa discount in a day across all restaurants'
                    WHEN EXISTS (
                        SELECT 1
                        FROM trans t2
                        WHERE t2.uid = t.uid
                            AND t2.delivery_type = 'SELF'
                            AND t2.distance_m < 50
                    ) THEN 'Distance between restaurant (' || t.rid || ') and delivery_address is less than 50 meters'
                    WHEN tc.total_count > 10 THEN 'Overall more than 10 transactions with gintaa discount'
                    ELSE NULL
                END AS reason,
                ROW_NUMBER() OVER (PARTITION BY t.uid ORDER BY t.uid) AS row_num
            FROM trans t
            LEFT JOIN aggregated_daily_counts adc ON t.uid = adc.uid
            LEFT JOIN aggregated_daily_counts_all_rids adc_all_rid ON t.uid = adc_all_rid.uid
            LEFT JOIN order_distances od ON t.uid = od.uid
            LEFT JOIN total_counts tc ON t.uid = tc.uid
        )
        INSERT INTO gintaa_food_order.fraudulent_transactions (uid, user_name, rid_and_day_wise_count, day_wise_total_count, order_id_distance, total_count, reason)
        SELECT
            rr.uid, 
            rr.user_name,
            rr.rid_and_day_wise_count,
            rr.day_wise_total_count,
            rr.order_id_distance,
            rr.total_count,
            rr.reason 
        FROM result_with_reason rr
        WHERE rr.reason IS NOT NULL
        AND rr.row_num = 1
        ORDER BY rr.uid;
        ''' 
        cursor.execute(sql_query, {'uid_list': tuple(blocked_uid_list), 'no_of_days': no_of_days})

        # Commit the changes
        conn_food_order.commit()

        # Close the cursor and connection
        cursor.close()
        conn_food_order.close()

        return "Table Updated successfully"
