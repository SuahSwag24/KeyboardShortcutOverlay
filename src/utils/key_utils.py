from pynput import keyboard
from config.settings import KEY_ORDER, SPECIAL_KEY_LABELS, VK_OEM_LABELS

#   Format keys from keycode to display
def format_keys(keys):
    result = []
    for key in keys:
        name = getattr(key, 'name', None)
        if name is not None:
            label = SPECIAL_KEY_LABELS.get(name) or name.replace("_", " ").title()
            result.append(label)
        elif hasattr(key, 'char') and key.char:
            result.append(key.char.upper())
        elif hasattr(key, 'vk'):
            result.append(VK_OEM_LABELS.get(key.vk, f"VK{key.vk}"))
        else:
            result.append(str(key))

    def sort_key(k):
        try:
            return KEY_ORDER.index(k)
        except ValueError:
            return len(KEY_ORDER)

    return " + ".join(sorted(result, key=sort_key))

#   Normalize ordinary VK into keys
def normalize_keys(key):
    if hasattr(key, 'vk'):
        if hasattr(key, 'char') and key.char:
            return keyboard.KeyCode(vk=key.vk, char=key.char)  # preserve char
        return keyboard.KeyCode.from_vk(key.vk)
    return key

#   Normalize modifier keys (Alt, Ctrl, Shift, etc.) into a consistent key string
def normalize_modifiers(modifiers):
    return frozenset(modifiers)