import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class PosWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current = [0.0, 0.0, 0.0]
        coords = ['X', 'Y', 'Z']
        self.entries = []
        for i, axis in enumerate(coords):
            tk.Label(self, text=f"{axis}:").pack(anchor='w', padx=5, pady=(5,0))
            entry = tk.Entry(self, width=15)
            entry.pack(anchor='w', padx=5, pady=2)
            entry.insert(0, "0.0")
            self.entries.append(entry)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("pos.save"), command=self._save)
        self.save_btn.pack(pady=10)
        self._save(silent=True)

    def _save(self, silent=False):
        try:
            vals = []
            for entry in self.entries:
                v = float(entry.get().strip())
                vals.append(v)
            self.current = vals
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("pos.error.invalid"))

    def get_nbt(self):
        return f'Pos:[{self.current[0]},{self.current[1]},{self.current[2]}]'