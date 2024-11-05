from read_sheet import ReadSheet
from call_api import CallApi
from secret_values import SecretValues


creds_dict, uid_sheet_url, date_sheet_url = SecretValues.read_sheet_secrets()
uid_df = ReadSheet.read_sheet(creds_dict, uid_sheet_url)
date_df = ReadSheet.read_sheet(creds_dict, date_sheet_url)
CallApi.call_api(uid_df, date_df)