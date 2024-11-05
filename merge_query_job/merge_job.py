from config import CONN_PATH


class MergeJob:

    def food_order_merge():
        client, project_id, time_period = CONN_PATH.big_query_conn()
        query_template = '''
        MERGE `{project_id}.data_warehouse.food_order` T
            USING (WITH RankedData AS (
            SELECT 
            payload.id, payload.uid, payload.order_id, payload.order_status, payload.payment_txn_id, 
            payload.payment_status, payload.delivery_address, payload.mobile, payload.cooking_instructions, 
            payload.amount_payable, payload.total_item_amount, payload.rid, payload.invoice_url, 
            payload.created_by, payload.created_date, payload.last_modified_by, payload.last_modified_date, 
            payload.user_name, payload.payment_gateway, payload.payment_order_data, payload.distance_haversine, 
            payload.distance_gmap, payload.restaurant_discount_amount, payload.delivery_charge, 
            payload.gintaa_discount_amount, payload.gst_amount, payload.gst_percent, payload.user_photo_url, 
            payload.restaurant_discount_percent, payload.gintaa_discount_percent, payload.order_date, 
            payload.cancellation_reason, payload.payout_amount, payload.restaurant_payment_id, 
            payload.coins_used, payload.coins_refunded, payload.sequence, payload.gintaa_discount_name, 
            payload.kot_url, payload.refund_status, payload.commission, payload.payment_gateway_charge, 
            payload.distance_geohash, payload.kitchen_preparation_time, payload.total_time, 
            payload.delivery_charge_payout, payload.invoice_small_url, payload.referral_discount_percent, 
            payload.referral_discount_amount, payload.delivery_partner, payload.delivery_type, 
            payload.takeaway_otp, payload.order_call_accept, payload.calculated_payout_amount, 
            payload.commission_without_gst, 
            ROW_NUMBER() OVER (PARTITION BY payload.id ORDER BY source_timestamp DESC) AS rnk 
            FROM `{project_id}.data_lake_landing_zone.food_order_landing_zone`
            WHERE source_metadata.change_type IN ('INSERT','UPDATE')
            AND source_timestamp > DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL {time_period} DAY)
            
        )
        SELECT 
            id, uid, order_id, order_status, payment_txn_id, payment_status, delivery_address, 
            mobile, cooking_instructions, amount_payable, total_item_amount, rid, invoice_url, 
            created_by, created_date, last_modified_by, last_modified_date, user_name, 
            payment_gateway, payment_order_data, distance_haversine, distance_gmap, 
            restaurant_discount_amount, delivery_charge, gintaa_discount_amount, gst_amount, 
            gst_percent, user_photo_url, restaurant_discount_percent, gintaa_discount_percent, 
            order_date, cancellation_reason, payout_amount, restaurant_payment_id, coins_used, 
            coins_refunded, sequence, gintaa_discount_name, kot_url, refund_status, commission, 
            payment_gateway_charge, distance_geohash, kitchen_preparation_time, total_time, 
            delivery_charge_payout, invoice_small_url, referral_discount_percent, 
            referral_discount_amount, delivery_partner, delivery_type, takeaway_otp, 
            order_call_accept, calculated_payout_amount, commission_without_gst
            FROM RankedData
            WHERE rnk = 1) S
        ON T.id = S.id 
        WHEN MATCHED THEN
        UPDATE SET
            T.id = S.id,
            T.uid = S.uid,
            T.order_id = S.order_id,
            T.order_status = S.order_status,
            T.payment_txn_id = S.payment_txn_id,
            T.payment_status = S.payment_status,
            T.delivery_address = S.delivery_address,
            T.mobile = S.mobile,
            T.cooking_instructions = S.cooking_instructions,
            T.amount_payable = S.amount_payable,
            T.total_item_amount = S.total_item_amount,
            T.rid = S.rid,
            T.invoice_url = S.invoice_url,
            T.created_by = S.created_by,
            T.created_date = S.created_date,
            T.last_modified_by = S.last_modified_by,
            T.last_modified_date = S.last_modified_date,
            T.user_name = S.user_name,
            T.payment_gateway = S.payment_gateway,
            T.payment_order_data = S.payment_order_data,
            T.distance_haversine = S.distance_haversine,
            T.distance_gmap = S.distance_gmap,
            T.restaurant_discount_amount = S.restaurant_discount_amount,
            T.delivery_charge = S.delivery_charge,
            T.gintaa_discount_amount = S.gintaa_discount_amount,
            T.gst_amount = S.gst_amount,
            T.gst_percent = S.gst_percent,
            T.user_photo_url = S.user_photo_url,
            T.restaurant_discount_percent = S.restaurant_discount_percent,
            T.gintaa_discount_percent = S.gintaa_discount_percent,
            T.order_date = S.order_date,
            T.cancellation_reason = S.cancellation_reason,
            T.payout_amount = S.payout_amount,
            T.restaurant_payment_id = S.restaurant_payment_id,
            T.coins_used = S.coins_used,
            T.coins_refunded = S.coins_refunded,
            T.sequence = S.sequence,
            T.gintaa_discount_name = S.gintaa_discount_name,
            T.kot_url = S.kot_url,
            T.refund_status = S.refund_status,
            T.commission = S.commission,
            T.payment_gateway_charge = S.payment_gateway_charge,
            T.distance_geohash = S.distance_geohash,
            T.kitchen_preparation_time = S.kitchen_preparation_time,
            T.total_time = S.total_time,
            T.delivery_charge_payout = S.delivery_charge_payout,
            T.invoice_small_url = S.invoice_small_url,
            T.referral_discount_percent = S.referral_discount_percent,
            T.referral_discount_amount = S.referral_discount_amount,
            T.delivery_partner = S.delivery_partner,
            T.delivery_type = S.delivery_type,
            T.takeaway_otp = S.takeaway_otp,
            T.order_call_accept = S.order_call_accept,
            T.calculated_payout_amount = S.calculated_payout_amount,
            T.commission_without_gst = S.commission_without_gst
        WHEN NOT MATCHED THEN
        INSERT (id, uid, order_id, order_status, payment_txn_id, payment_status, 
            delivery_address, mobile, cooking_instructions, amount_payable, 
            total_item_amount, rid, invoice_url, created_by, created_date, 
            last_modified_by, last_modified_date, user_name, payment_gateway, 
            payment_order_data, distance_haversine, distance_gmap, 
            restaurant_discount_amount, delivery_charge, gintaa_discount_amount, 
            gst_amount, gst_percent, user_photo_url, restaurant_discount_percent, 
            gintaa_discount_percent, order_date, cancellation_reason, payout_amount, 
            restaurant_payment_id, coins_used, coins_refunded, sequence, 
            gintaa_discount_name, kot_url, refund_status, commission, 
            payment_gateway_charge, distance_geohash, kitchen_preparation_time, 
            total_time, delivery_charge_payout, invoice_small_url, 
            referral_discount_percent, referral_discount_amount, delivery_partner, 
            delivery_type, takeaway_otp, order_call_accept, calculated_payout_amount, 
            commission_without_gst) VALUES ( 
            id, uid, order_id, order_status, payment_txn_id, payment_status, delivery_address, 
            mobile, cooking_instructions, amount_payable, total_item_amount, rid, invoice_url, 
            created_by, created_date, last_modified_by, last_modified_date, user_name, 
            payment_gateway, payment_order_data, distance_haversine, distance_gmap, 
            restaurant_discount_amount, delivery_charge, gintaa_discount_amount, gst_amount, 
            gst_percent, user_photo_url, restaurant_discount_percent, gintaa_discount_percent, 
            order_date, cancellation_reason, payout_amount, restaurant_payment_id, coins_used, 
            coins_refunded, sequence, gintaa_discount_name, kot_url, refund_status, commission, 
            payment_gateway_charge, distance_geohash, kitchen_preparation_time, total_time, 
            delivery_charge_payout, invoice_small_url, referral_discount_percent, 
            referral_discount_amount, delivery_partner, delivery_type, takeaway_otp, 
            order_call_accept, calculated_payout_amount, commission_without_gst);
        '''

        query = query_template.format(project_id=project_id, time_period=time_period)

        # Run the query
        query_job = client.query(query)

        # Wait for the query to finish
        query_job.result()

        return "food_order table updated successfully"
