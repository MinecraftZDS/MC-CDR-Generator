import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class EnchantableWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_value = 1

        tk.Label(self, text=bc.get_lang_text("enchantable.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.value_entry = tk.Entry(self, width=10)
        self.value_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("enchantable.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            val = int(self.value_entry.get().strip())
            if val < 1:
                raise ValueError
            self.current_value = val
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("enchantable.error.invalid"))

    def get_nbt(self):
        return f'enchantable={{value:{self.current_value}}}'