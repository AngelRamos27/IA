#herramienta para scrapear imagenes de marketplace
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import time
from urllib.parse import urlparse

# Configuración del navegador
def get_driver():
    print("Inicializando navegador...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def download_image(url, folder):
    try:
        print(f"Descargando imagen: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen descargada: {filepath}")
    except Exception as e:
        print(f"Error al descargar la imagen {url}: {e}")

def scrape_facebook_marketplace(search_query, download_folder, max_images=10):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Carpeta creada: {download_folder}")

    driver = get_driver()
    downloaded_urls = set()  

    try:
        # Navegar al Marketplace de Facebook
        url = f"https://www.facebook.com/marketplace/morelia/search?query={search_query}"
        print(f"Navegando a {url}")
        driver.get(url)
        time.sleep(5)  

        # Desplazar para cargar más publicaciones
        print("Desplazándose para cargar publicaciones...")
        for _ in range(5):  
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)

        print("Buscando imágenes...")
        image_elements = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in image_elements if img.get_attribute("src") is not None]
        print(f"Se encontraron {len(image_urls)} imágenes")

        # Descargar las imágenes
        for img_url in image_urls:
            if img_url not in downloaded_urls:  
                download_image(img_url, download_folder)
                downloaded_urls.add(img_url)  
                if len(downloaded_urls) >= max_images:
                    print("Se alcanzó el límite de imágenes")
                    break
            else:
                print(f"Imagen duplicada omitida: {img_url}")

    except Exception as e:
        print(f"Error durante el scraping: {e}")
    finally:
        driver.quit()
        print("Navegador cerrado")

# Uso del script
if __name__ == "__main__":
    search_term = "tsuru 1" 
    output_folder = "imagenes_marketplace"
    scrape_facebook_marketplace(search_term, output_folder, max_images=500)
