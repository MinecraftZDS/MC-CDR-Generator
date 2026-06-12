import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class UseCooldownWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_group = ""
        self.current_seconds = 0.0

        tk.Label(self, text=bc.get_lang_text("use_cooldown.group_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.group_entry = tk.Entry(self, width=30)
        self.group_entry.pack(fill='x', padx=5, pady=2)

        tk.Label(self, text=bc.get_lang_text("use_cooldown.seconds_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.seconds_entry = tk.Entry(self, width=10)
        self.seconds_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("use_cooldown.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        group = self.group_entry.get().strip()
        if not group:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("use_cooldown.error.group_empty"))
            return
        try:
            sec = float(self.seconds_entry.get().strip())
            if sec <= 0:
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("use_cooldown.error.invalid_seconds"))
            return
        self.current_group = group
        self.current_seconds = sec
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_group:
            return ""
        return f'use_cooldown={{cooldown_group:"{self.current_group}",seconds:{self.current_seconds}}}'