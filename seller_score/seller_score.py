from generate_score import GENERATE_SCORE
from write_in_db import WRITE_IN_DB
df=GENERATE_SCORE().gen_score()
print(WRITE_IN_DB().update_db(df))