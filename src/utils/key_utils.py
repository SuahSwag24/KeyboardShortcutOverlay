from pynput import keyboard
from config.settings import KEY_ORDER, VK_OEM_LABELS

def format_keys(keys):
    result = []

    for key in keys:
        if isinstance(key, keyboard.Key):
            result.append(key.name.capitalize())
        elif key.char is not None:
            result.append(key.char.upper())
        else:
            vk_label = VK_OEM_LABELS.get(key.vk)
            result.append(vk_label)
        
    def sort_keys(k):
        try:
            return KEY_ORDER.index(k)
        except ValueError:
            return len(KEY_ORDER)
        
    return " + ".join(sorted(result, key=sort_keys))

#   Normalize modifier keys (Alt, Ctrl, Shift, etc.) into a consistent key string
def normalize_modifiers(modifiers):
    return frozenset(modifiers)