#Herramienta para saber que tan parecidos son entre sí los textos (tener mayor diversidad de info)

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import glob
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words_espanol = stopwords.words('spanish')  #

def leer_pdf(ruta):
    texto = ""
    try:
        with open(ruta, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            for pagina in lector.pages:
                texto += pagina.extract_text()
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
    return texto

def leer_txt(ruta):
    texto = ""
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
    return texto

def recopilar_documentos(directorio):
    documentos = []
    archivos = glob.glob(os.path.join(directorio, "*.pdf")) + glob.glob(os.path.join(directorio, "*.txt"))
    
    for archivo in archivos:
        if archivo.endswith(".pdf"):
            documentos.append(leer_pdf(archivo))
        elif archivo.endswith(".txt"):
            documentos.append(leer_txt(archivo))
    return documentos, archivos

# Calcular la similitud coseno
def calcular_similitud(documentos):
    # Convertir los documentos en vectores TF-IDF usando las stop words en español
    vectorizador = TfidfVectorizer(stop_words=stop_words_espanol)
    tfidf_matriz = vectorizador.fit_transform(documentos)
    
    # Calcular la similitud coseno
    similitud = cosine_similarity(tfidf_matriz)
    return similitud

def main():
    directorio = "C:/Users/angel/OneDrive/Escritorio/IA/LenguajeNatural/judicial"  
    documentos, nombres_archivos = recopilar_documentos(directorio)

    if not documentos:
        print("No se encontraron documentos.")
        return

    similitud = calcular_similitud(documentos)

    print("Matriz de similitud coseno:")
    for i, nombre1 in enumerate(nombres_archivos):
        for j, nombre2 in enumerate(nombres_archivos):
            if i != j:
                print(f"Similitud entre '{os.path.basename(nombre1)}' y '{os.path.basename(nombre2)}': {similitud[i][j]:.2f}")

if __name__ == "__main__":
    main()
