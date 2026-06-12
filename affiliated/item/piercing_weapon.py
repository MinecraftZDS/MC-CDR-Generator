import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class PiercingWeaponWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.deals_knockback = False
        self.dismounts = False

        # 复选框
        self.knockback_var = tk.BooleanVar(value=False)
        self.dismounts_var = tk.BooleanVar(value=False)

        tk.Checkbutton(self, text=bc.get_lang_text("piercing_weapon.deals_knockback"),
                       variable=self.knockback_var).pack(anchor='w', padx=5, pady=2)
        tk.Checkbutton(self, text=bc.get_lang_text("piercing_weapon.dismounts"),
                       variable=self.dismounts_var).pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("piercing_weapon.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        self.deals_knockback = self.knockback_var.get()
        self.dismounts = self.dismounts_var.get()
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'piercing_weapon={{deals_knockback:{str(self.deals_knockback).lower()},dismounts:{str(self.dismounts).lower()}}}'