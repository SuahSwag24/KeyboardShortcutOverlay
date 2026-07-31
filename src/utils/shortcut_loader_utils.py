import json
import os

from config.settings import MODIFIER_MAP
from utils.path_util import get_config_dir, resolve_shortcut_path

GLOBAL_PATH = os.path.join(get_config_dir(), "shortcut_lists", "global.json")
CATEGORY_PATH = os.path.join(get_config_dir(), "application_category.json")

with open(CATEGORY_PATH) as f:
    _APP_MAP: dict = json.load(f)


def load_shortcuts(path):
    resolved_path = resolve_shortcut_path(path)
    with open(resolved_path, "r") as f:
        raw = json.load(f)

    flat = {}
    grouped = {}

    for action in raw:
        flat[action["combo"]] = action["description"]
        
        mod = action["modifier"]
        if mod not in grouped:
            grouped[mod] = []
        grouped[mod].append((action["combo"], action["description"]))

    return flat, grouped
    
def build_grouped_shortcuts(grouped):
    result = {}
    for key_combo, actions in grouped.items():
        keys = frozenset(
            MODIFIER_MAP[k] for k in key_combo.split("+") if k in MODIFIER_MAP
        )
        result[keys] = actions
    return result

_global_flat, _global_grouped = load_shortcuts(GLOBAL_PATH)

SHORTCUTS_FLAT = dict(_global_flat)
SHORTCUTS = build_grouped_shortcuts(_global_grouped)

def reload_shortcuts(path=None):
    global SHORTCUTS_FLAT, SHORTCUTS, _global_flat, _global_grouped

    _global_flat, _global_grouped = load_shortcuts(GLOBAL_PATH)
    resolved = resolve_shortcut_path(path) if path else None
    is_global = (not resolved) or (os.path.abspath(resolved) == os.path.abspath(GLOBAL_PATH))

    if is_global:
        SHORTCUTS_FLAT = dict(_global_flat)
        SHORTCUTS = build_grouped_shortcuts(_global_grouped)
    else:
        context_flat, context_grouped = load_shortcuts(resolved)
        merged_flat = {**_global_flat, **context_flat}
        merged_grouped = {}
        
        for mod, actions in _global_grouped.items():
            merged_grouped[mod] = dict(actions)

        for mod, actions in context_grouped.items():
            if mod not in merged_grouped:
                merged_grouped[mod] = {}
            merged_grouped[mod].update(dict(actions))

        for mod in merged_grouped:
            merged_grouped[mod] = list(merged_grouped[mod].items())

        SHORTCUTS_FLAT = merged_flat
        SHORTCUTS = build_grouped_shortcuts(merged_grouped)

def get_shortcut_path(executable):
    app = _APP_MAP.get(executable)
    if app:
        return resolve_shortcut_path(app["shortcut_file"])
    else:
        return None