import os

def ensure_folder(folder):
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

