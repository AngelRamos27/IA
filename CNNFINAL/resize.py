#herramienta para convertir imagenes a 80x80
import os
import cv2

def redimensionar_imagenes(directorio_entrada, directorio_salida, ancho=80, alto=80):
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    for nombre_archivo in os.listdir(directorio_entrada):
        ruta_archivo = os.path.join(directorio_entrada, nombre_archivo)

        if os.path.isfile(ruta_archivo) and nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
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
    directorio_entrada = "C:/Users/angel/OneDrive/Escritorio/IaA/IA/EjerciciosPy/CNNFINAL/dataset/d"  
    directorio_salida = "C:/Users/angel/OneDrive/Escritorio/IaA/IA/EjerciciosPy/CNNFINAL/dataset/d/m"    

    redimensionar_imagenes(directorio_entrada, directorio_salida, ancho=80, alto=80)