import os

def remove_empty_subfolders(path):
    # Przechodzi przez wszystkie podfoldery w danym katalogu
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            # Sprawdza czy folder jest pusty
            if not os.listdir(dir_path):
                # Usuwa pusty folder
                os.rmdir(dir_path)
                print(f"Usunięto pusty folder: {dir_path}")

# Ścieżka do katalogu głównego 'data'
data_path = 'data'

# Usuwanie pustych podfolderów
remove_empty_subfolders(data_path)
