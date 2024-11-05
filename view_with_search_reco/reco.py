from recommendation_cal import RECOMMENDATION_CAL
from write_db import INSERT_TO_DB
df=RECOMMENDATION_CAL().reco()
print(INSERT_TO_DB().write_to_db(df))
