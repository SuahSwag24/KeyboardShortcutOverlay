import json

from config.settings import MODIFIER_MAP

GLOBAL_PATH = "KeyboardShortcutOverlay/src/config/shortcut_lists/global.json"
CATEGORY_PATH = "KeyboardShortcutOverlay/src/config/application_category.json"

with open(CATEGORY_PATH) as f:
    _APP_MAP: dict = json.load(f)


def load_shortcuts(path):
    with open(path, "r") as f:
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
        keys = frozenset(MODIFIER_MAP[k] for k in key_combo.split("+"))
        result[keys] = actions
    return result

_global_flat, _global_grouped = load_shortcuts(GLOBAL_PATH)

SHORTCUTS_FLAT = dict(_global_flat)
SHORTCUTS = build_grouped_shortcuts(_global_grouped)

def load_context_shortcuts(context_path):
    global SHORTCUTS_FLAT, SHORTCUTS

    context_flat, context_grouped = load_shortcuts(context_path)
    merged_flat = {**_global_flat, **context_flat}

    merged_grouped = {}
    for mod, actions in _global_grouped.items():
        merged_grouped[mod] = list(actions)
    for mod, actions in context_grouped.items():
        if mod in merged_grouped:
            merged_grouped[mod].extend(actions)
        else:
            merged_grouped[mod] = list(actions)

    SHORTCUTS_FLAT = merged_flat
    SHORTCUTS = build_grouped_shortcuts(merged_grouped)

def reset_to_global():
    global SHORTCUTS_FLAT, SHORTCUTS
    SHORTCUTS_FLAT = dict(_global_flat)
    SHORTCUTS = build_grouped_shortcuts(_global_grouped)

def get_shortcut_path(executable):
    app = _APP_MAP.get(executable)
    if app:
        return app["shortcut_file"]
    else:
        return None