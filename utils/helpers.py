import json
import os

def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
def init_json_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)