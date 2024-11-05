from fetch_data import FetchData
from update_delivery_time import UpdateDeliveryTime

data_to_insert=FetchData.fetch_data()
print(UpdateDeliveryTime.update_delivery_time(data_to_insert))