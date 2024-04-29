import os

def remove_empty_subfolders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Empty dir has been removed: {dir_path}")

data_path = 'data'

remove_empty_subfolders(data_path)
