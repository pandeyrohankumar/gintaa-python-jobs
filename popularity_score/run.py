from popularity_score import POPULARITY_SCORE
from write_db import INSERT_TO_DB
df=POPULARITY_SCORE().generate_score()
print(INSERT_TO_DB().write_to_db(df))