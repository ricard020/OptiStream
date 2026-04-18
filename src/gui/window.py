import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

# Relative imports assuming this runs as a module or package
try:
    from ..logic.ffmpeg_handler import compress_video_task
    from ..utils.helpers import center_window, set_app_icon
    from .styles import configure_styles, COLORS
except ImportError:
    # Fallback for direct execution/IDE testing
    from src.logic.ffmpeg_handler import compress_video_task
    from src.utils.helpers import center_window, set_app_icon
    from src.gui.styles import configure_styles, COLORS

class VideoCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OptiStream | Máxima calidad, mínimo peso")
        
        # Helper utilities
        center_window(self.root)
        set_app_icon(self.root)
        configure_styles(self.root)
        
        self.root.configure(bg=COLORS["bg"])

        # Variables
        self.file_path = tk.StringVar()
        self.crf_value = tk.IntVar(value=28)
        self.quality_mode = tk.StringVar(value="balanced")
        self.status_var = tk.StringVar(value="Esperando archivo...")
        self.original_size_var = tk.StringVar(value="")
        self.final_result_var = tk.StringVar(value="")
        self.timer_var = tk.StringVar(value="Tiempo restante: --:--")
        
        self.input_controls = [] 

        self.create_widgets()

    def create_widgets(self):
        main = ttk.Frame(self.root, style="TFrame")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        lbl_header = ttk.Label(main, text="OptiStream", style="Header.TLabel")
        lbl_header.pack(anchor="center", pady=(0, 15))

        # File Selection
        self.create_file_selection(main)

        # Settings
        self.create_settings_area(main)
        
        # Actions
        self.create_actions_area(main)

        # Status
        self.create_status_area(main)

    def create_file_selection(self, parent):
        file_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        file_card.pack(fill=tk.X, pady=(0, 15))
        
        file_row = ttk.Frame(file_card, style="Card.TFrame")
        file_row.pack(fill=tk.X)
        
        self.entry_file = ttk.Entry(file_row, textvariable=self.file_path, state='readonly', font=("Segoe UI", 9))
        self.entry_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.btn_browse = ttk.Button(file_row, text="Seleccionar", style="Secondary.TButton", command=self.browse_file, takefocus=False)
        self.btn_browse.pack(side=tk.RIGHT)
        
        lbl_size = ttk.Label(file_card, textvariable=self.original_size_var, style="Info.TLabel")
        lbl_size.pack(anchor="w", pady=(8, 0))

        self.input_controls.extend([self.btn_browse, self.entry_file])

    def create_settings_area(self, parent):
        settings_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        settings_card.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(settings_card, text="Calidad de Compresión", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 5))
        
        info_text = "Nota: Si eliges un CRF menor (mejor calidad) que el del original, el peso podría aumentar."
        ttk.Label(settings_card, text=info_text, style="Info.TLabel", wraplength=550).pack(anchor="w", pady=(0, 8))
        
        ttk.Separator(settings_card, orient='horizontal').pack(fill=tk.X, pady=(0, 10))

        presets_frame = ttk.Frame(settings_card, style="Card.TFrame")
        presets_frame.pack(fill=tk.X)

        self.rb1 = ttk.Radiobutton(presets_frame, text="Alta Calidad (CRF 23)", variable=self.quality_mode, value="high", command=self.toggle_manual, takefocus=False)
        self.rb1.pack(anchor="w", pady=1)
        self.rb2 = ttk.Radiobutton(presets_frame, text="Equilibrado (CRF 28)", variable=self.quality_mode, value="balanced", command=self.toggle_manual, takefocus=False)
        self.rb2.pack(anchor="w", pady=1)
        self.rb3 = ttk.Radiobutton(presets_frame, text="Alta Compresión (CRF 32)", variable=self.quality_mode, value="compressed", command=self.toggle_manual, takefocus=False)
        self.rb3.pack(anchor="w", pady=1)
        self.rb4 = ttk.Radiobutton(presets_frame, text="Manual", variable=self.quality_mode, value="manual", command=self.toggle_manual, takefocus=False)
        self.rb4.pack(anchor="w", pady=(1, 5))

        self.input_controls.extend([self.rb1, self.rb2, self.rb3, self.rb4])

        self.manual_frame = ttk.Frame(settings_card, style="Card.TFrame")
        self.lbl_crf_val = ttk.Label(self.manual_frame, text=f"Valor CRF: {self.crf_value.get()}")
        self.lbl_crf_val.pack(anchor="w")
        
        self.scale_crf = ttk.Scale(self.manual_frame, from_=0, to=51, variable=self.crf_value, command=self.update_crf_label)
        self.scale_crf.pack(fill=tk.X)
        self.input_controls.append(self.scale_crf)

    def create_actions_area(self, parent):
        action_area = ttk.Frame(parent, style="TFrame")
        action_area.pack(fill=tk.X, pady=(5, 0))

        self.btn_compress = ttk.Button(action_area, text="Iniciar Compresión", style="Primary.TButton", command=self.start_compression_thread, takefocus=False)
        self.btn_compress.pack(fill=tk.X, pady=(0, 8))
        self.input_controls.append(self.btn_compress)

        self.progress_bar = ttk.Progressbar(parent, mode='determinate', style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

    def create_status_area(self, parent):
        status_frame = ttk.Frame(parent, style="TFrame")
        status_frame.pack(fill=tk.X)
        ttk.Label(status_frame, textvariable=self.status_var, style="Info.TLabel", background=COLORS["bg"]).pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.timer_var, style="Timer.TLabel").pack(side=tk.RIGHT)
        
        ttk.Label(parent, textvariable=self.final_result_var, style="Result.TLabel").pack(anchor="center", pady=(5, 0))

    def toggle_controls(self, state):
        for widget in self.input_controls:
            try:
                widget.configure(state=state)
            except: pass

    def toggle_manual(self):
        if self.quality_mode.get() == "manual":
            self.manual_frame.pack(fill=tk.X, pady=5)
        else:
            self.manual_frame.pack_forget()

    def update_crf_label(self, e=None):
        self.lbl_crf_val.config(text=f"Valor CRF: {int(self.crf_value.get())}")

    def get_crf(self):
        m = self.quality_mode.get()
        return {"high": 23, "balanced": 28, "compressed": 32}.get(m, int(self.crf_value.get()))

    def browse_file(self):
        f = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv")])
        if f:
            self.file_path.set(f)
            try:
                s = os.path.getsize(f) / (1024*1024)
                self.original_size_var.set(f"Tamaño actual: {s:.2f} MB")
            except: pass
            self.final_result_var.set("")
            self.status_var.set("Listo")
            self.timer_var.set("Tiempo restante: --:--")
            self.progress_bar["value"] = 0

    def start_compression_thread(self):
        if not self.file_path.get(): return
        
        self.toggle_controls('disabled')
        self.status_var.set("Iniciando motor FFmpeg...")
        self.final_result_var.set("")
        self.progress_bar["mode"] = "determinate"
        self.progress_bar["value"] = 0
        
        threading.Thread(target=self.run_compression_task, daemon=True).start()

    def run_compression_task(self):
        inp = self.file_path.get()
        out = os.path.splitext(inp)[0] + "_opt" + os.path.splitext(inp)[1]
        
        compress_video_task(
            inp=inp,
            out=out,
            crf=self.get_crf(),
            on_progress=self.on_progress_callback,
            on_complete=self.on_complete_callback,
            on_error=self.on_error_callback
        )

    def on_progress_callback(self, percent, eta):
        self.root.after(0, lambda: self.update_progress_ui(percent, eta))

    def on_complete_callback(self, inp, out):
        self.root.after(0, lambda: self.finish_ui(inp, out))

    def on_error_callback(self, msg):
        self.root.after(0, lambda: self.fail_ui(msg))

    def update_progress_ui(self, percent, eta):
        self.progress_bar["value"] = percent
        self.timer_var.set(f"Faltan: {eta}")
        self.status_var.set(f"Comprimiendo: {int(percent)}%")

    def finish_ui(self, inp, out):
        self.toggle_controls('normal')
        self.status_var.set("Finalizado")
        self.timer_var.set("Completado")
        self.progress_bar["value"] = 100
        
        try:
            s_orig = os.path.getsize(inp)
            s_final = os.path.getsize(out)
            
            txt = f"Final: {s_final/(1024*1024):.2f} MB"
            
            if s_final > s_orig:
                inc = ((s_final - s_orig)/s_orig)*100
                txt += f" (+{inc:.1f}%) "
                messagebox.showwarning("Aumento de Tamaño", 
                    f"El archivo creció {inc:.1f}%.\nLa calidad original era baja.\nUsa 'Alta Compresión' la próxima vez.\n")
            else:
                diff_p = ((s_orig - s_final)/s_orig)*100
                txt += f" (Reducción: {diff_p:.1f}%)"
                messagebox.showinfo("Éxito", f"Video comprimido correctamente.\nGuardado en la carpeta original.\n")
            
            self.final_result_var.set(txt)
        except: 
            self.toggle_controls('normal')

    def fail_ui(self, msg):
        self.toggle_controls('normal')
        self.status_var.set("Error")
        messagebox.showerror("Error", msg)
