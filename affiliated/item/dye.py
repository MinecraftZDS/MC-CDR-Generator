import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class DyeWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_color = "white"

        colors = [
            "white", "orange", "magenta", "light_blue", "yellow",
            "lime", "pink", "gray", "light_gray", "cyan",
            "purple", "blue", "brown", "green", "red", "black"
        ]

        tk.Label(self, text=bc.get_lang_text("dye.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.color_combo = ttk.Combobox(self, values=colors, state='readonly', width=20)
        self.color_combo.pack(padx=5, pady=5)
        if colors:
            self.color_combo.current(0)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("dye.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        color = self.color_combo.get().strip()
        if not color:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("dye.error.empty"))
            return
        self.current_color = color
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'dye="{self.current_color}"'