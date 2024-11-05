from sql_init_new import SQL_INIT
from  write_in_elastic_new import ELASTIC


conn, offer_stats_df,detail_df = SQL_INIT().sql_conn()

from calculate_trending_new import CALCULATE_TRENDING
new_top_scores,old_top_scores, top_categories= CALCULATE_TRENDING().score_calc(offer_stats_df,detail_df)

print (new_top_scores)

print(old_top_scores)

# print (top_categories)

ELASTIC().elastic_push(new_top_scores,old_top_scores)
# print("Done")



