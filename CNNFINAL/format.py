#herramienta para convertir a formatos válidos las imagenes
import os
from PIL import Image

def convert_images_to_jpg(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Itera a través de los archivos del directorio
    for root, _, files in os.walk(input_dir):
        for file in files:
            # Extensiones válidas para la conversión
            if file.lower().endswith(('.png', '.jpeg', '.bmp', '.tiff', '.gif', '.webp')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.jpg')
                
                try:
                    # Abre la imagen y la convierte a RGB
                    with Image.open(input_path) as img:
                        rgb_image = img.convert('RGB')  # Convertir a formato compatible con JPG
                        rgb_image.save(output_path, 'JPEG')
                        print(f"Convertida: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Error al convertir {input_path}: {e}")

input_directory = r"C:\Users\angel\OneDrive\Escritorio\IaA\IA\EjerciciosPy\CNNFINAL\dataset\tsuru1"
output_directory = r"C:\Users\angel\OneDrive\Escritorio\IaA\IA\EjerciciosPy\CNNFINAL\dataset\tsuru11"

convert_images_to_jpg(input_directory, output_directory)
