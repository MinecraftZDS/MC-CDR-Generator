import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class MapColorWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_color = 0

        tk.Label(self, text=bc.get_lang_text("map_color.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.color_entry = tk.Entry(self, width=10)
        self.color_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("map_color.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            val = int(self.color_entry.get().strip())
            if 0 <= val <= 16777215:
                self.current_color = val
                if not silent:
                    messagebox.showinfo(bc.get_lang_text("success.title"),
                                        bc.get_lang_text("msgbox.info.saved"))
            else:
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("map_color.error.invalid"))

    def get_nbt(self):
        return f'map_color={self.current_color}'