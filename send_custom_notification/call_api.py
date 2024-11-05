import requests
from secret_values import SecretValues
from datetime import datetime
import logging


class CallApi:

    @staticmethod
    def call_api(uid_df, date_df):

        today = datetime.today().strftime('%d/%m/%Y')
        
        today_row = date_df[date_df['date'] == today]
        
        if not today_row.empty:
            event_type = ''.join(today_row.iloc[0]['type'].split())
        else:
            print("No matching date found.")
            return

        gintaa_api_key, location, project = SecretValues.call_api_secrets()

        data_list = uid_df['uid'].tolist()

        url = f"https://{location}-{project}.cloudfunctions.net/customNotificationEventInternal?size=1000&time=5000&type={event_type}"
        logging.info(url)
        headers = {
            "Content-Type": "application/json",
            "gintaa-api-key": gintaa_api_key
        }

        payload = {
            "data": data_list
        }

        response = requests.post(url, json=payload, headers=headers)

        
        print(f"Status Code: {response.status_code}")

        try:
            response_data = response.json()
            print(response_data)
        except:
            None
