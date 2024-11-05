from restaurant_top_selling_food import RESTAURANT_TOP_SELLING_FOOD
from write_db import WRITE_DB
df=RESTAURANT_TOP_SELLING_FOOD().restaurant_top_selling_food()
print(WRITE_DB().write_to_db(df))