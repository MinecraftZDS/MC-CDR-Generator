import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class StateWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_state = "idle"
        states = ["idle", "rolling", "scared"]

        tk.Label(self, text=bc.get_lang_text("state.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.combo = ttk.Combobox(self, values=states, state='readonly', width=10)
        self.combo.pack(anchor='w', padx=5, pady=2)
        self.combo.current(0)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("state.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        self.current_state = self.combo.get().strip()
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'State:"{self.current_state}"'