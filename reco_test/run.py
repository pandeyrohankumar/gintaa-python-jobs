from createdata import CREATEDATA
from write_db import INSERT_TO_DB
df=CREATEDATA().createdata()
print(INSERT_TO_DB().write_to_db(df))