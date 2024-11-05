import os
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


creds_dict_str = os.getenv('GOOGLE_APPLICATION_KEY')

if creds_dict_str is None:
    raise EnvironmentError("GOOGLE_APPLICATION_KEY environment variable not set")

creds_dict = json.loads(creds_dict_str)

def write_to_google_sheet_by_url(creds_dict, sheet_url, dataframe):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)

    worksheet.clear()

    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
    print("Data saved to Google Sheet successfully.")

def read_restaurant_data_from_sheet(creds_dict, sheet_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0) 

    data = worksheet.get_all_records() 
    return data

read_sheet_url = 'https://docs.google.com/spreadsheets/d/1XjI5CoHZl_l6fvERsfc3l_diYQfr0jzBYK0L85SAVDo/edit?gid=0#gid=0'
write_sheet_url = 'https://docs.google.com/spreadsheets/d/1tGf-UkxHpZiVQ1zkVGsGIwR3QtWPjAfDEJ5N1ckc1qc/edit?gid=0#gid=0'

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

restaurant_data = read_restaurant_data_from_sheet(creds_dict, read_sheet_url)

all_food_data = []

for restaurant in restaurant_data:
    try:
        restaurant_name = restaurant.get('Restaurant Name')
        url = restaurant.get('URL')
        
        if not url or not restaurant_name:
            continue  

        driver.get(url)
        time.sleep(5) 

        scroll_count = 10
        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        food_data = []
        items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="normal-dish-item"]')
        
        for item in items:
            try:
                food_name = item.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.cjJTeQ.sc-hIUJlX.gCYyvX').text
                price_container = item.find_element(By.CSS_SELECTOR, 'div.sc-eZkCL.erfDC')
                prices = price_container.find_elements(By.CSS_SELECTOR, 'div.sc-aXZVg')

                original_price = prices[0].text if prices else 'N/A'
                discounted_price = prices[1].text if len(prices) > 1 else original_price 

                food_data.append({
                    'Restaurant Name': restaurant_name,
                    'Food Name': food_name,
                    'Original Price': original_price,
                    'Discounted Price': discounted_price
                })
            except (AttributeError, IndexError):
                continue
        
        all_food_data.extend(food_data)
    except Exception as e:
        print(f"Failed to extract data from {url} ({restaurant_name}): {str(e)}")

df = pd.DataFrame(all_food_data)

if not df.empty:
    write_to_google_sheet_by_url(creds_dict, write_sheet_url, df)
else:
    print("No data extracted.")

driver.quit()
