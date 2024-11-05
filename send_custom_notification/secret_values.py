import os


class SecretValues:

    @staticmethod
    def call_api_secrets():

        gintaa_api_key = os.getenv('API_KEY')
        location = os.getenv('API_LOCATION')
        project = os.getenv('PROJECT')

        return gintaa_api_key, location, project
    
    def read_sheet_secrets():

        creds_dict = os.getenv('GOOGLE_APPLICATION_KEY')
        uid_sheet_url = os.getenv('UID_SHEET_URL')
        date_sheet_url = os.getenv('DATE_SHEET_URL')

        return creds_dict, uid_sheet_url,date_sheet_url