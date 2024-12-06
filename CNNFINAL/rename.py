import os

def rename_files(folder_path, base_name, start_number, increment):
    """
    Renames files in a folder with a new numbering pattern.
    
    :param folder_path: Path to the folder containing files to rename.
    :param base_name: Base name for the files (e.g., 'tsuru1_').
    :param start_number: The starting number for renaming (e.g., 555).
    :param increment: The increment for numbering (e.g., 1).
    """
    try:
        files = sorted(os.listdir(folder_path))
        current_number = start_number

        for file_name in files:
            # Get the file extension
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                extension = os.path.splitext(file_name)[1]

                # Construct the new file name
                new_name = f"{base_name}{current_number:05d}{extension}"
                new_file_path = os.path.join(folder_path, new_name)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_name} -> {new_name}")

                # Increment the number
                current_number += increment

    except Exception as e:
        print(f"Error: {e}")

# Usage
folder_path = r"C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/dataset/bmw330e"  # Cambia esta ruta a tu carpeta
base_name = "bmw330i_"
start_number = 000
increment = 1

rename_files(folder_path, base_name, start_number, increment)
