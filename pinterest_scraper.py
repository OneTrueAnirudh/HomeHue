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

chromedriver_autoinstaller.install()

USERNAME = "anirudh.t2021@vitstudent.ac.in"
PASSWORD = "101 No_0b!"
MIN_WIDTH = 200
MIN_HEIGHT = 200

def login_to_pinterest(driver):
    driver.get('https://www.pinterest.com/login/')
    time.sleep(3)

    username_input = driver.find_element(By.NAME, "id")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

def filter_image_by_size(url):
    try:
        response = requests.get(url,timeout=10)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        if width >= MIN_WIDTH and height >= MIN_HEIGHT:
            return True
        else:
            return False
    except Exception as e:
        print(f"Failed to process image: {e}")
        return False

def search_pinterest(driver, search_query, image_count):
    search_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search"]')))
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    image_urls = set()
    while len(image_urls) < image_count:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        images = soup.find_all('img', {'src': True})

        for img in images:
            if len(image_urls) >= image_count:
                break
            img_url = img['src']
            if img_url.startswith('http') and filter_image_by_size(img_url):
                image_urls.add(img_url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    return list(image_urls)

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            img_path = os.path.join(folder_path, f'image_{timestamp}.jpg')

            img.save(img_path)
            print(f"Downloaded {img_path}")
        except Exception as e:
            print(f"Failed to download image: {e}")

def scrape_pinterest(search_query, image_count, folder_path):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_to_pinterest(driver)
        image_urls = search_pinterest(driver, search_query, image_count)
        download_images(image_urls, folder_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = "room interior design ideas"
    image_count = 10
    folder_path = r"pinterest_images"
    scrape_pinterest(search_query, image_count, folder_path)
