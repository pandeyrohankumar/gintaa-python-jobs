from restaurant_pos import RestaurantPos
from write_to_bigquery import WriteToBigquery

try:
    df = RestaurantPos().get_data()

    result = WriteToBigquery().write_to_bq(df)

    # print(result)

except Exception as e:
    print(f"An error occurred: {str(e)}")
