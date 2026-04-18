import os
import tkinter as tk

def center_window(window, w=600, h=580):
    """Centers the window on the screen."""
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = int((sw/2) - (w/2))
    y = int((sh/2) - (h/2))
    window.geometry(f"{w}x{h}+{x}+{y}")
    window.resizable(False, False)

def set_app_icon(window, app_id='antigravity.optistream.v1'):
    """Sets the application icon and taskbar grouping ID."""
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        
        # Path relative to this file: src/utils/helpers.py -> ../../assets/logo/logo-ico.ico
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        icon_path = os.path.join(project_root, "assets", "logo", "logo-ico.ico")
        
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
    except Exception:
        pass
