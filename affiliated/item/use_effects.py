import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class UseEffectsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.can_sprint = False
        self.interact_vibrations = False
        self.speed_multiplier = 0.2

        # 复选框
        self.sprint_var = tk.BooleanVar(value=False)
        self.vibrations_var = tk.BooleanVar(value=False)

        tk.Checkbutton(self, text=bc.get_lang_text("use_effects.can_sprint"),
                       variable=self.sprint_var).pack(anchor='w', padx=5, pady=2)
        tk.Checkbutton(self, text=bc.get_lang_text("use_effects.interact_vibrations"),
                       variable=self.vibrations_var).pack(anchor='w', padx=5, pady=2)

        tk.Label(self, text=bc.get_lang_text("use_effects.speed_multiplier")).pack(anchor='w', padx=5, pady=(5, 0))
        self.multiplier_entry = tk.Entry(self, width=10)
        self.multiplier_entry.pack(anchor='w', padx=5, pady=2)
        self.multiplier_entry.insert(0, "0.2")

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("use_effects.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            mult = float(self.multiplier_entry.get().strip())
            if not (0 <= mult <= 1):
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("use_effects.error.invalid_multiplier"))
            return
        self.can_sprint = self.sprint_var.get()
        self.interact_vibrations = self.vibrations_var.get()
        self.speed_multiplier = mult
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'use_effects={{can_sprint:{str(self.can_sprint).lower()},interact_vibrations:{str(self.interact_vibrations).lower()},speed_multiplier:{self.speed_multiplier}}}'