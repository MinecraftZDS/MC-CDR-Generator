import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class FireWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_value = 0
        tk.Label(self, text=bc.get_lang_text("fire.label")).pack(anchor='w', padx=5, pady=(10,0))
        self.entry = tk.Entry(self, width=10)
        self.entry.pack(anchor='w', padx=5, pady=2)
        self.entry.insert(0, "0")
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("fire.save"), command=self._save)
        self.save_btn.pack(pady=10)
        self._save(silent=True)

    def _save(self, silent=False):
        try:
            val = int(self.entry.get().strip())
            self.current_value = val
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("fire.error.invalid"))

    def get_nbt(self):
        return f'Fire:{self.current_value}'