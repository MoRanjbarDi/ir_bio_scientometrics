import os

def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    return True

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
