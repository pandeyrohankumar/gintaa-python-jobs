import os

class SecretValues:

    @staticmethod
    def read_sheet_secrets():

        creds_dict = os.getenv('GOOGLE_APPLICATION_KEY')
        sheet_url = os.getenv('DATE_SHEET_URL')

        return creds_dict, sheet_url
    
    @staticmethod
    def scheduler_secrets():

        creds_dict = os.getenv('GOOGLE_APPLICATION_KEY')
        location = os.getenv('SCHEDULER_LOCATION')
        project = os.getenv('PROJECT')

        return creds_dict, location, project
