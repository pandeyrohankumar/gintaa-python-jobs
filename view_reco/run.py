from config import CONN_PATH
from view_reco import VIEW_RECO
from write_db import INSERT_TO_DB
run_type=CONN_PATH().run_type()
print(run_type)
if (run_type=='Overall'):
    df=VIEW_RECO().view_reco_overall()
    print(INSERT_TO_DB().write_to_db(df))
elif (run_type=='Intraday'):
    df_to_insert,df_to_update=VIEW_RECO().view_reco_intraday()
    print(INSERT_TO_DB().update_db(df_to_insert,df_to_update))