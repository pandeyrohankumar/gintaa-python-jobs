from impression_count import IMPRESSION
from write_db import INSERT_TO_DB
df=IMPRESSION().impression_count()
print(df)
print(INSERT_TO_DB().write_to_db(df))