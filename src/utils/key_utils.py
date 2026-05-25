from pynput import keyboard
from config.settings import KEY_ORDER, MODIFIER_NORMALIZE

#   format_keys
def format_keys(keys):
    result = []
    for key in keys:
        try:
            result.append(key.name.replace("_l", "").replace("_r", "").capitalize())
        except AttributeError:
            if hasattr(key, 'vk'):
                try:
                    result.append(key.char.upper() if key.char else chr(key.vk))
                except (AttributeError, TypeError):
                    result.append(chr(key.vk).upper())
            else:
                result.append(str(key))
        
    def sort_key(k):
        try:
            return KEY_ORDER.index(k)
        except ValueError:
            return len(KEY_ORDER)
        
    return " + ".join(sorted(result, key=sort_key))

#   normalize
def normalize_keys(key):
    if hasattr(key, 'vk'):
        return keyboard.KeyCode.from_vk(key.vk)
    return key

#   normalize_modifiers
def normalize_modifiers(modifiers):
    return frozenset(MODIFIER_NORMALIZE.get(key , key) for key in modifiers)