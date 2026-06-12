import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class WeaponWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.disable_seconds = 0.0
        self.damage_per_attack = 0

        tk.Label(self, text=bc.get_lang_text("weapon.disable_blocking_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.seconds_entry = tk.Entry(self, width=10)
        self.seconds_entry.pack(anchor='w', padx=5, pady=2)

        tk.Label(self, text=bc.get_lang_text("weapon.damage_per_attack_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.damage_entry = tk.Entry(self, width=10)
        self.damage_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("weapon.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            seconds = float(self.seconds_entry.get().strip())
            if seconds < 0:
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("weapon.error.invalid_seconds"))
            return

        try:
            damage = int(self.damage_entry.get().strip())
            if damage < 0:
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("weapon.error.invalid_damage"))
            return

        self.disable_seconds = seconds
        self.damage_per_attack = damage
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'weapon={{disable_blocking_for_seconds:{self.disable_seconds},item_damage_per_attack:{self.damage_per_attack}}}'