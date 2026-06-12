import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class FoodWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.can_always_eat = False
        self.nutrition = 1
        self.saturation = 1

        # can_always_eat
        self.always_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("food.can_always_eat"),
                       variable=self.always_var).pack(anchor='w', padx=5, pady=2)

        # nutrition
        tk.Label(self, text=bc.get_lang_text("food.nutrition")).pack(anchor='w', padx=5, pady=2)
        self.nutrition_entry = tk.Entry(self, width=10)
        self.nutrition_entry.pack(anchor='w', padx=5, pady=2)

        # saturation
        tk.Label(self, text=bc.get_lang_text("food.saturation")).pack(anchor='w', padx=5, pady=2)
        self.saturation_entry = tk.Entry(self, width=10)
        self.saturation_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("food.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            nutrition = int(self.nutrition_entry.get().strip() or "1")
            if nutrition <= 0:
                raise ValueError
            saturation = int(self.saturation_entry.get().strip() or "1")
            if saturation <= 0:
                raise ValueError
            self.can_always_eat = self.always_var.get()
            self.nutrition = nutrition
            self.saturation = saturation
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("food.error.invalid"))

    def get_nbt(self):
        return f'food={{can_always_eat:{str(self.can_always_eat).lower()},nutrition:{self.nutrition},saturation:{self.saturation}}}'