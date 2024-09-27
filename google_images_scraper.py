import os
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

# Automatically install and use the latest version of ChromeDriver
chromedriver_autoinstaller.install()

def create_directory(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def is_valid_image_size(img_url, min_size=(200, 200)):
    if "encrypted-tbn0.gstatic.com" in img_url:
        # Skip thumbnail URLs from Google
        print(f"Skipping thumbnail URL: {img_url}")
        return False

    try:
        response = requests.get(img_url, timeout=5)
        img = Image.open(BytesIO(response.content))
        if img.size[0] >= min_size[0] and img.size[1] >= min_size[1]:
            return True
        return False
    except Exception as e:
        print(f"Error checking image size: {e}")
        return False

def download_image(img_url, folder_name, img_number):
    try:
        response = requests.get(img_url, timeout=5)
        img = Image.open(BytesIO(response.content))
        img_name = os.path.join(folder_name, f"image_{img_number}.jpg")
        img.save(img_name)
        print(f"Downloaded: {img_name}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def search_google_images(driver, search_query, image_count):
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Scroll and collect image URLs dynamically until we have enough
    image_urls = set()
    scroll_pause_time = 2
    max_scroll_attempts = 20  # Limit the number of scrolls

    scroll_attempts = 0
    while len(image_urls) < image_count and scroll_attempts < max_scroll_attempts:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        images = soup.find_all('img', {'src': True})

        for img in images:
            if len(image_urls) >= image_count:
                break
            img_url = img['src']
            if img_url.startswith('http') and is_valid_image_size(img_url):
                image_urls.add(img_url)

        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        scroll_attempts += 1

    if len(image_urls) < image_count:
        print(f"Warning: Only found {len(image_urls)} valid images after {scroll_attempts} scrolls.")

    return list(image_urls)

def scrape_google_images(query, num_images, folder_name):
    # Set up Selenium and open Google Images
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if you don't want a browser window
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.google.com/imghp')  # Directly open Google Images
    time.sleep(2)  # Let Google Images load

    # Perform search and gather image URLs
    img_urls = search_google_images(driver, query, num_images)
    driver.quit()

    # Create directory and download images
    create_directory(folder_name)
    
    for idx, img_url in enumerate(img_urls):
        download_image(img_url, folder_name, idx + 1)

    print(f"Downloaded {len(img_urls)} images to {folder_name}")

# Usage
search_query = "interior design"
num_of_images = 10
download_folder = r"C:\HomeHue\google_images"

scrape_google_images(search_query, num_of_images, download_folder)
