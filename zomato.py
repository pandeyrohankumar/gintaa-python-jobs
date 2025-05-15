from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import openpyxl

# Initialize the Chrome WebDriver (provide the correct path to chromedriver)
service = Service("chromedriver.exe")  # Change the path to your ChromeDriver
driver = webdriver.Chrome(service=service)  # Change the path to your ChromeDriver

# Function to search for branch name and pincode and get the Zomato rating
def search_zomato(branch_name, pincode, city="Bangalore"):
    # Open the Zomato website
    driver.get("https://www.zomato.com")

    # Allow the page to load
    time.sleep(5)

    # Close any popup if present
    try:
        close_popup = driver.find_element(By.CLASS_NAME, 'sc-1yzxt5f-2')
        close_popup.click()
    except:
        pass
    
    # Select the location (City, e.g., Bangalore)
    location_input = driver.find_element(By.XPATH, "//input[@placeholder='Search for restaurant, cuisine or a dish']")
    location_input.click()
    location_input.send_keys(city)
    location_input.send_keys(Keys.ENTER)

    # Allow time for location selection to be processed
    time.sleep(3)

    # Search for the branch name and pincode
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for restaurant, cuisine or a dish']")
    search_query = f"{branch_name} {pincode}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)

    # Allow time for the search results to load
    time.sleep(5)

    # Try to scrape the restaurant rating
    try:
        rating_element = driver.find_element(By.CLASS_NAME, "sc-1q7bklc-1")
        rating = rating_element.text
    except:
        rating = "Rating not found"
    
    return rating

# Function to read branch and pincode from an Excel file and write the result to another Excel file
def process_excel_files(input_file, output_file):
    # Load the input Excel file
    input_wb = openpyxl.load_workbook(input_file)
    input_sheet = input_wb.active

    # Create the output Excel file (or overwrite if it exists)
    output_wb = openpyxl.Workbook()
    output_sheet = output_wb.active

    # Copy the header row to the output sheet
    output_sheet.append([cell.value for cell in input_sheet[1]])

    # Iterate through each row in the input sheet, starting from row 2 (assuming row 1 is the header)
    for row in input_sheet.iter_rows(min_row=2, values_only=True):
        restaurant_name, branch_name, pincode, address, latitude, longitude, rating, phone_number = row

        # Get the Zomato rating by searching using branch name and pincode
        new_rating = search_zomato(branch_name, pincode)

        # Append the data along with the new rating to the output sheet
        output_sheet.append([restaurant_name, branch_name, pincode, address, latitude, longitude, new_rating, phone_number])
    
    # Save the output Excel file
    output_wb.save(output_file)

# Main function to run the script
def main():
    input_file = "result.xlsx"  # Replace with the name of your input file
    output_file = "output_with_zomato_ratings.xlsx"  # Replace with your desired output file

    # Process the Excel files
    process_excel_files(input_file, output_file)

    # Close the browser when done
    driver.quit()

if __name__ == "__main__":
    main()
