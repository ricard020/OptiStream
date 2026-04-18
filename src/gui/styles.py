import tkinter.ttk as ttk

COLORS = {
    "bg": "#f4f6f9",
    "panel": "#ffffff",
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "text": "#1f2937",
    "text_light": "#6b7280",
    "border": "#e5e7eb"
}

def configure_styles(root=None):
    """Configures the Tkinter styles using the defined color palette."""
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["panel"], relief="flat")
    
    style.configure("TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=("Segoe UI", 10))
    style.configure("Header.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 16, "bold"))
    style.configure("SubHeader.TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=("Segoe UI", 10, "bold"))
    style.configure("Info.TLabel", background=COLORS["panel"], foreground=COLORS["text_light"], font=("Segoe UI", 9))
    style.configure("Timer.TLabel", background=COLORS["bg"], foreground=COLORS["text_light"], font=("Segoe UI", 9))
    style.configure("Result.TLabel", background=COLORS["bg"], foreground=COLORS["primary"], font=("Segoe UI", 11, "bold"))

    # Buttons
    style.configure("Primary.TButton", background=COLORS["primary"], foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0, padding=8)
    style.map("Primary.TButton", background=[("active", COLORS["primary_hover"])])

    style.configure("Secondary.TButton", background="#e5e7eb", foreground=COLORS["text"], font=("Segoe UI", 9), borderwidth=0, padding=6)
    style.map("Secondary.TButton", background=[("active", "#d1d5db")])

    style.configure("TRadiobutton", background=COLORS["panel"], foreground=COLORS["text"], font=("Segoe UI", 10))
    style.configure("Horizontal.TProgressbar", background=COLORS["primary"], troughcolor="#e5e7eb", borderwidth=0)
    style.configure("TEntry", padding=5, relief="flat", borderwidth=1, fieldbackground="white")
    style.configure("TSeparator", background=COLORS["border"])
