import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class CustomNameVisibleWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.enabled = False
        self.var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("entity.custom_name_visible"), variable=self.var).pack(pady=10)
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("entity.save"), command=self._save)
        self.save_btn.pack(pady=5)
        self._save(silent=True)

    def _save(self, silent=False):
        self.enabled = self.var.get()
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'CustomNameVisible:{"1" if self.enabled else "0"}'