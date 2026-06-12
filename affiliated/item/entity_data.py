import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import affiliated.kernel.basic_components as bc

class EntityDataWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_id = ""
        self.current_nbt = ""

        # 实体 ID 输入框
        tk.Label(self, text=bc.get_lang_text("entity_data.id_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.id_entry = tk.Entry(self, width=40)
        self.id_entry.pack(fill='x', padx=5, pady=2)

        # 其他实体组件（可换行）
        tk.Label(self, text=bc.get_lang_text("entity_data.nbt_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.nbt_text = ScrolledText(self, height=10, wrap='word', font=('Consolas', 10))
        self.nbt_text.pack(fill='both', expand=True, padx=5, pady=5)

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("entity_data.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        id_val = self.id_entry.get().strip()
        nbt_val = self.nbt_text.get('1.0', 'end-1c').strip()

        if not id_val:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("entity_data.error.id_empty"))
            return

        self.current_id = id_val
        self.current_nbt = nbt_val

        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_id:
            return ""
        if self.current_nbt:
            return f'entity_data={{id:"{self.current_id}", {self.current_nbt}}}'
        else:
            return f'entity_data={{id:"{self.current_id}"}}'