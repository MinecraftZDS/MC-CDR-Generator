import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class MinimumAttackChargeWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_charge = 0.0

        tk.Label(self, text=bc.get_lang_text("minimum_attack_charge.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.charge_entry = tk.Entry(self, width=10)
        self.charge_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("minimum_attack_charge.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            val = float(self.charge_entry.get().strip())
            if val < 0.0 or val > 1.0:
                raise ValueError
            self.current_charge = val
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("minimum_attack_charge.error.invalid"))

    def get_nbt(self):
        # 格式化浮点数，保留必要精度，去掉末尾零
        formatted = f"{self.current_charge:.2f}".rstrip('0').rstrip('.')
        return f'minimum_attack_charge={formatted}'