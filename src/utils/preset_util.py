import json
import os
from utils.path_util import get_config_dir

SHORTCUT_LISTS_DIR = os.path.join(get_config_dir(), "shortcut_lists")
CATEGORY_PATH = os.path.join(get_config_dir(), "application_category.json")

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