from food_recommendation import FoodRecommendation
from write_db import WriteDb
user_type_df=FoodRecommendation().user_type_recommendation()
print(WriteDb().write_to_user_food_recommendation_type(user_type_df))
popular_food_df=FoodRecommendation().popular_food()
print(WriteDb().write_to_popular_foods(popular_food_df))
user_cuisine_reco_df=FoodRecommendation().user_cuisine_recommendation()
print(WriteDb().write_to_user_food_recommendation_cuisine(user_cuisine_reco_df))
