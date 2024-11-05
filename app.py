from sql_init import SQL_INIT


conn, offer_stats_df = SQL_INIT().sql_conn()

from calculate_trending import CALCULATE_TRENDING
top_scores, top_categories= CALCULATE_TRENDING().score_calc(offer_stats_df)

print (top_scores)
print (top_categories)

from AllJSONresp import FETCH_ALL_JSON
all_response_offer,all_response_category= FETCH_ALL_JSON().allfieldsfromAPI(top_scores,top_categories)

from write_to_db import INSERT_TO_DB
message=INSERT_TO_DB().write_to_db(conn, all_response_offer, all_response_category)
print (message)
