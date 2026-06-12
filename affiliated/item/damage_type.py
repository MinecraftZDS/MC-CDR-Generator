import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import affiliated.kernel.basic_components as bc

class DamageTypeWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_type = ""

        # 加载预设伤害类型
        self.damage_types = self._load_damage_types()

        tk.Label(self, text=bc.get_lang_text("damage_type.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.type_combo = ttk.Combobox(self, values=self.damage_types, state='readonly', width=30)
        self.type_combo.pack(fill='x', padx=5, pady=2)
        if self.damage_types:
            self.type_combo.current(0)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("damage_type.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _load_damage_types(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('damage_types', [])
        except:
            return []

    def _save(self, silent=False):
        val = self.type_combo.get().strip()
        if not val:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("damage_type.error.empty"))
            return
        self.current_type = val
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_type:
            return ""
        return f'damage_type={self.current_type}'