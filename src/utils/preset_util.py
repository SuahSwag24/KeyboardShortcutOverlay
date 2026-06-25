import json
import os

SHORTCUT_LISTS_DIR = os.path.join(os.path.dirname(__file__), "..", "config", "shortcut_lists")
CATEGORY_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "application_category.json")

#   Load preset JSON into lists
def _load_preset(path):
    with open(path, "r") as f:
        return json.load(f)
    
#   Save list of shortcut to JSON
def _save_preset(path, new_data):
    with open(path, "w") as f:
        json.dump(new_data, f, indent=2)

def _load_category():
    with open(CATEGORY_PATH, "r") as f:
        return json.load(f)
    
def _save_category(new_data):
    with open(CATEGORY_PATH, "w") as f:
        return json.dump(new_data, f, indent=4)