import win32gui
import win32process
import psutil

def get_focused_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return None, None, None
        
        window_title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        executable = process.name()

        return hwnd, window_title, executable
    except Exception as e:
        print(f"Error getting focused window: {e}")
        return None, None, None