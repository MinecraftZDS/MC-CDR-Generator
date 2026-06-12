import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class IntangibleProjectileWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        tk.Label(self, text=bc.get_lang_text("intangible_projectile.label")).pack(pady=10)
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("intangible_projectile.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return "intangible_projectile={}"