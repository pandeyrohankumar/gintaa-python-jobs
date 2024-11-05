import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json


class ReadSheet:

    @staticmethod
    def read_sheet(creds_dict, sheet_url):

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]        
        creds_dict = json.loads(creds_dict)        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)        
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        return df
  