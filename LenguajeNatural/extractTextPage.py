#Herramienta para extraer el texto de páginas web (por ejemplo, de noticias)

import requests
from bs4 import BeautifulSoup

def extraer_texto_relevante(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Buscar el contenedor principal del artículo (ajustar según el sitio web)
        articulo = soup.find('article')  
        if not articulo:
            articulo = soup.find('div', class_='main-content')  
        if not articulo:
            articulo = soup  # Si no se encuentra, usar todo el HTML
        
        # Eliminar barras laterales, anuncios y contenido no relevante
        for sidebar in articulo.find_all(['aside', 'nav', 'footer']):
            sidebar.decompose()  # Elimina estos elementos del DOM
        
        for no_relevante in articulo.find_all('div', class_=['sidebar', 'related', 'ads', 'promo', 'banner']):
            no_relevante.decompose()
        
        # Extraer encabezados y párrafos del artículo principal
        contenido = []
        for encabezado in articulo.find_all(['h1', 'h2', 'h3']):
            contenido.append(encabezado.get_text(strip=True))
        for parrafo in articulo.find_all('p'):
            contenido.append(parrafo.get_text(strip=True))
        
        texto_relevante = "\n".join(contenido)
        return texto_relevante

    except requests.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return None

if __name__ == "__main__":
    url = "https://www.reuters.com/latam/domestico/GOOBCT4I4BKRXJNMUC6ACNTH6Q-2024-11-21/"
    
    print("Extrayendo contenido...")
    texto = extraer_texto_relevante(url)
    
    if texto:
        print("\nTexto extraído:")
        print(texto)
        
        archivo = "C:/Users/angel/OneDrive/Escritorio/IA/LenguajeNatural/txtArticulosJudicial/articulo_extraidoJudicial_32.txt"
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"\nEl texto se ha guardado en: {archivo}")
    else:
        print("No se pudo extraer el contenido.")
