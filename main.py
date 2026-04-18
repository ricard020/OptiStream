import tkinter as tk
from src.gui.window import VideoCompressorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressorApp(root)
    root.mainloop()
