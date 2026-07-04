from pynput import keyboard
from config.settings import KEY_ORDER, VK_OEM_LABELS
from exceptions.keyboard_exception import UnknownKeyError

def format_keys(keys):
    result = []

    for key in keys:
        if isinstance(key, keyboard.Key):
            result.append(key.name.replace("_", " ").title())
        elif key.char is not None:
            result.append(key.char.upper())
        else:
            vk_label = VK_OEM_LABELS.get(key.vk)
            if vk_label is None:
                raise UnknownKeyError(f"Unknown key with vk={key.vk!r}")
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

def parse_combo(combo) -> list[str]:
    return [k.strip() for k in combo.split("+")]