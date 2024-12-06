# heramienta para hacer efecto espejo de una imagén y rotar de cabeza y obtener distintas perspectivas de una imagén
import os
from PIL import Image

def process_images_with_mirror_and_upside_down(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if not filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            continue
        
        try:
            with Image.open(file_path) as img:
                img.save(os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_original{os.path.splitext(filename)[1]}"))

                # Crear imagen con efecto espejo horizontal
                mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                mirrored_img.save(os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_mirror{os.path.splitext(filename)[1]}"))

                # Crear imagen rotada de cabeza (180 grados)
                upside_down_img = img.rotate(180)
                upside_down_img.save(os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_upside_down{os.path.splitext(filename)[1]}"))

                print(f"Procesado: {filename}")

        except Exception as e:
            print(f"Error procesando {filename}: {e}")


# Ruta del directorio de entrada y salida
input_directory = "C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/dataset/bmw330e"
output_directory = "C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/dataset/bmw330eFull"

process_images_with_mirror_and_upside_down(input_directory, output_directory)