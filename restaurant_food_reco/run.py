from restaurant_food_reco import RESTAURANT_FOOD_RECO
from write_db import WRITE_DB
df=RESTAURANT_FOOD_RECO().restaurant_food_reco()
print(WRITE_DB().write_to_db(df))