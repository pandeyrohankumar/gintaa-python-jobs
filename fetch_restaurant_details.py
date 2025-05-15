import pandas as pd
import requests
import time
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = '*********'

def search_restaurant_branches(restaurant_name, city='Bangalore'):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{restaurant_name}, {city}",
        "key": API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result.get('results', [])
    return []

def get_place_details(place_id):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number",
        "key": API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return result['result'].get('formatted_phone_number', 'No phone number found')
    return 'Not found'

df = pd.read_excel('Restaurant names.xlsx') 

all_branches = []
batch_size = 100
total_restaurants = len(df)
num_batches = math.ceil(total_restaurants / batch_size)

def save_batch_to_excel(batch_data, start_idx, end_idx):
    batch_df = pd.DataFrame(batch_data)
    file_name = f'restaurants_{start_idx + 1}-{end_idx}.xlsx'
    batch_df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

for batch_number in range(num_batches):
    print(f"Processing batch {batch_number + 1} of {num_batches}")
    
    start_index = batch_number * batch_size
    end_index = min(start_index + batch_size, total_restaurants)
    
    batch_restaurants = df.iloc[start_index:end_index]
    
    batch_branches = []
    
    for index, row in batch_restaurants.iterrows():
        restaurant_name = row['Restaurant Name']
        
        if not isinstance(restaurant_name, str):
            print(f"Ignoring entry at row {index} due to non-string restaurant name: {restaurant_name}")
            continue
        
        branches = search_restaurant_branches(restaurant_name)
        
        if branches:
            for branch in branches:
                place_id = branch['place_id']
                branch_name = branch.get('name', 'Unknown')
                address = branch.get('formatted_address', 'No address found')
                location = branch['geometry']['location']
                lat = location.get('lat', None)
                lng = location.get('lng', None)
                rating = branch.get('rating', 'No rating')
                
                if rating != 'No rating' and float(rating) <= 3.5:
                    print(f"Ignoring branch {branch_name} due to low rating ({rating})")
                    continue

                phone_number = get_place_details(place_id)
                
                batch_branches.append({
                    'Restaurant Name': restaurant_name,
                    'Branch Name': branch_name,
                    'Address': address,
                    'Latitude': lat,
                    'Longitude': lng,
                    'Rating': rating,
                    'Phone Number': phone_number
                })
                
                print(f"Processed branch {branch_name}: Address={address}, Lat={lat}, Lng={lng}, Rating={rating}, Phone={phone_number}")
        
        else:
            print(f"No branches found for {restaurant_name}")
        
        time.sleep(1)
    
    save_batch_to_excel(batch_branches, start_index, end_index)

print("Processing completed.")
