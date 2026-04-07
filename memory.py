import json, os

FILE = "memory.json"

def load():
    if not os.path.exists(FILE):
        return {}
    
    # Check if file is empty before loading
    if os.path.getsize(FILE) == 0:
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty dict if file is corrupted

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)