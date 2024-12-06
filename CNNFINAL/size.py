import os
import cv2

def redimensionar_imagenes(directorio_entrada, directorio_salida, ancho=80, alto=80):
    """
    Redimensiona todas las imágenes en un directorio al tamaño especificado y las guarda en otro directorio.
    
    Args:
        directorio_entrada (str): Ruta del directorio donde están las imágenes originales.
        directorio_salida (str): Ruta del directorio donde se guardarán las imágenes redimensionadas.
        ancho (int): Ancho deseado de las imágenes redimensionadas.
        alto (int): Alto deseado de las imágenes redimensionadas.
    """
    # Crear el directorio de salida si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    # Recorrer todos los archivos en el directorio de entrada
    for nombre_archivo in os.listdir(directorio_entrada):
        ruta_archivo = os.path.join(directorio_entrada, nombre_archivo)

        # Verificar si es un archivo válido de imagen
        if os.path.isfile(ruta_archivo) and nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                # Leer la imagen
                imagen = cv2.imread(ruta_archivo)

                # Redimensionar la imagen
                imagen_redimensionada = cv2.resize(imagen, (ancho, alto))

                # Guardar la imagen redimensionada en el directorio de salida
                ruta_salida = os.path.join(directorio_salida, nombre_archivo)
                cv2.imwrite(ruta_salida, imagen_redimensionada)
                print(f"Procesado: {nombre_archivo}")
            except Exception as e:
                print(f"Error procesando {nombre_archivo}: {e}")

if __name__ == "__main__":
    directorio_entrada = "C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/dataset3/bmw318d"  # Cambia esto por la ruta de tu directorio de entrada
    directorio_salida = "C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/dataset3/bmw318dd"    # Cambia esto por la ruta de tu directorio de salida

    redimensionar_imagenes(directorio_entrada, directorio_salida, ancho=80, alto=80)
