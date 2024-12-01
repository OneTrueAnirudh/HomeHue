import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import chromedriver_autoinstaller
from datetime import datetime

# Automatically install the ChromeDriver if not already installed
chromedriver_autoinstaller.install()

# Pinterest login credentials
USERNAME = "enter ur username"
PASSWORD = "enter ur passwd"
# Minimum dimensions for images to be downloaded
MIN_WIDTH = 200
MIN_HEIGHT = 200

def login_to_pinterest(driver):
    driver.get('https://www.pinterest.com/login/')  # Navigate to Pinterest login page
    time.sleep(3)

    # Locate the login input fields
    username_input = driver.find_element(By.NAME, "id")
    password_input = driver.find_element(By.NAME, "password")

    # Enter the username and password, then submit the form
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Wait for the login process to complete
    time.sleep(5)

def filter_image_by_size(url):
    try:
        response = requests.get(url, timeout=10)  # Fetch the image
        img = Image.open(BytesIO(response.content))  # Load the image into memory
        width, height = img.size  # Get the image dimensions
        
        # Return True if the image meets the minimum size requirements
        if width >= MIN_WIDTH and height >= MIN_HEIGHT:
            return True
        else:
            return False
    except Exception as e:
        # Handle errors such as network issues or unsupported image formats
        print(f"Failed to process image: {e}")
        return False

def search_pinterest(driver, search_query, image_count):
    # Locate the search box and enter the search query
    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search"]')))
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)  # Submit the search query
    time.sleep(3)

    image_urls = set()  # Use a set to avoid duplicate URLs

    # Scroll through the page to extract images until we reach the desired count
    while len(image_urls) < image_count:
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the page source
        images = soup.find_all('img', {'src': True})  # Find all image tags with a valid source

        # Process each image, applying size filtering and adding to the URL list
        for img in images:
            if len(image_urls) >= image_count:
                break
            img_url = img['src']
            if img_url.startswith('http') and filter_image_by_size(img_url):
                image_urls.add(img_url)  # Add valid image URL to the set

        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    return list(image_urls)

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)  # Fetch the image data
            img = Image.open(BytesIO(response.content))  # Load image into memory

            # Generate a timestamp-based unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            img_path = os.path.join(folder_path, f'image_{timestamp}.jpg')

            # Save the image to the specified path
            img.save(img_path)
            print(f"Downloaded {img_path}")
        except Exception as e:
            # Handle errors such as network failures or unsupported formats
            print(f"Failed to download image: {e}")

def scrape_pinterest(search_query, image_count, folder_path):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window for better visibility

    driver = webdriver.Chrome(options=chrome_options)  # Initialize the Chrome driver

    try:
        login_to_pinterest(driver)  # Log in to Pinterest
        image_urls = search_pinterest(driver, search_query, image_count)  # Perform the image search
        download_images(image_urls, folder_path)  # Download the images
    finally:
        driver.quit()  # Ensure the browser is closed after the scraping process

# if __name__ == "__main__":
#     search_query = "interior design room ideas"
#     image_count = 10
#     folder_path = r"pinterest_images"
#     scrape_pinterest(search_query, image_count, folder_path)