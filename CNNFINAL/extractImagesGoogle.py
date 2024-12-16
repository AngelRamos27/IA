#herramienta para scrapear imagenes de google 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from hashlib import md5

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(url, folder_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_hash = md5(response.content).hexdigest()
            file_path = os.path.join(folder_name, f"{image_hash}.jpg")
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {file_path}")
            else:
                print("Duplicate image skipped.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def search_and_download_images(search_query, num_images, output_folder):
    # Set up Selenium
    driver = webdriver.Chrome()  
    driver.get("https://images.google.com")

    # Search for the query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    image_urls = set()
    while len(image_urls) < num_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Find image elements
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            try:
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    image_urls.add(src)
                if len(image_urls) >= num_images:
                    break
            except Exception as e:
                print(f"Error fetching image URL: {e}")

    print(f"Found {len(image_urls)} images. Downloading...")

    create_folder(output_folder)
    for url in image_urls:
        download_image(url, output_folder)

    driver.quit()

if __name__ == "__main__":
    query = input("Enter the search query: ")
    number_of_images = int(input("Enter the number of images to download: "))
    folder = r"C:\Users\angel\OneDrive\Escritorio\IaA\IA\EjerciciosPy\CNNFINAL\cam"
    search_and_download_images(query, number_of_images, folder)
