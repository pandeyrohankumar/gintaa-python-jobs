from fraud import FRAUD
from write_db import INSERT_TO_DB
df=FRAUD().fraud_transaction()
print(INSERT_TO_DB().write_to_db(df))