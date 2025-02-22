import os

def remove_temp_file(file_path):
    """Elimina el archivo temporal después de procesarlo."""
    if os.path.exists(file_path):
        os.remove(file_path)
