import ctypes
from ctypes import wintypes

def get_taskbar_height():
    taskbar_hwnd = ctypes.windll.user32.FindWindowW(u"Shell_TrayWnd", None)
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(rect))
    return rect.bottom - rect.top

def get_window_title_bar_size():
    title_bar_height = ctypes.windll.user32.GetSystemMetrics(4)  # SM_CYCAPTION
    border_height = ctypes.windll.user32.GetSystemMetrics(6)  # SM_CYSIZEFRAME
    unknown_offset = -1
    return title_bar_height + border_height + unknown_offset

def get_total_window_height():
    window_height = get_window_title_bar_size()
    taskbar_height = get_taskbar_height()
    return window_height + taskbar_height
