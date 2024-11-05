import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import json
from secret_values import SecretValues


class CheckDate:

    @staticmethod
    def check_date():

        creds_dict, sheet_url = SecretValues.read_sheet_secrets()
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]        
        creds_dict = json.loads(creds_dict)        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)        
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        today_date = datetime.now().strftime('%d/%m/%Y')
        
        if today_date in df['date'].values:
            time_str = df.loc[df['date'] == today_date, 'time'].values[0]
            if pd.isnull(time_str):
                raise ValueError("Time value is null for today's date")
            time_obj = datetime.strptime(time_str, '%H:%M')
            
            return time_obj.minute, time_obj.hour
        else:
            return None
  