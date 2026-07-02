import os
import sys

def get_config_dir():
    if getattr(sys, 'frozen', False):
        # Running as a compiled executable
        base_dir = os.path.dirname(sys.executable)
        return os.path.join(base_dir, "config")
    else:
        # Running in development
        # __file__ is src/utils/path_util.py -> go up two levels to get the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(project_root, "config")

def resolve_shortcut_path(path):
    if not path:
        return path
    if "config/shortcut_lists/" in path:
        filename = os.path.basename(path)
        return os.path.join(get_config_dir(), "shortcut_lists", filename)
    return path
