#Herramienta para encontrar articulos con palabras clave 

from googlesearch import search

def buscar_articulos(keywords, num_resultados=10):
    try:
        resultados = search(keywords, num_results=num_resultados, lang="es")
        return list(resultados)
    except Exception as e:
        print(f"Error al realizar la búsqueda: {e}")
        return []

def guardar_en_txt(articulos, archivo="C:/Users/angel/OneDrive/Escritorio/IA/LenguajeNatural/resultados.txt"):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("Resultados de la búsqueda:\n\n")
            for idx, url in enumerate(articulos, start=1):
                f.write(f"{idx}. {url}\n")
        print(f"Resultados guardados en el archivo: {archivo}")
    except Exception as e:
        print(f"Error al guardar los resultados en el archivo: {e}")

if __name__ == "__main__":
    articulos = buscar_articulos("Reforma poder judicial noticias", 10)
    if articulos:
        print("\nArtículos encontrados:")
        for idx, url in enumerate(articulos, start=1):
            print(f"{idx}. {url}")
        guardar_en_txt(articulos)
    else:
        print("No se encontraron resultados.")
