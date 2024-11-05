from rhi_score import RHI_SCORE
from write_db import WRITE_DB
df,blacklisted_rids=RHI_SCORE().generate_score()
print(WRITE_DB().write_to_bq(df,blacklisted_rids))
print(WRITE_DB().write_to_db(df,blacklisted_rids))