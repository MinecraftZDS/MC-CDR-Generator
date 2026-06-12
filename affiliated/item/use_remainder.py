import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import affiliated.kernel.basic_components as bc

class UseRemainderWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_id = ""
        self.current_count = 1
        self.current_components = ""

        # ID 输入框
        tk.Label(self, text=bc.get_lang_text("use_remainder.id_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.id_entry = tk.Entry(self, width=40)
        self.id_entry.pack(fill='x', padx=5, pady=2)

        # Count 输入框
        tk.Label(self, text=bc.get_lang_text("use_remainder.count_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.count_entry = tk.Entry(self, width=10)
        self.count_entry.pack(anchor='w', padx=5, pady=2)
        self.count_entry.insert(0, "1")

        # Components 多行文本框
        tk.Label(self, text=bc.get_lang_text("use_remainder.components_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.components_text = ScrolledText(self, height=6, wrap='word', font=('Consolas', 10))
        self.components_text.pack(fill='both', expand=True, padx=5, pady=5)

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("use_remainder.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        id_val = self.id_entry.get().strip()
        if not id_val:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("use_remainder.error.id_empty"))
            return
        try:
            count_val = int(self.count_entry.get().strip())
            if count_val < 0:
                raise ValueError
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("use_remainder.error.count_invalid"))
            return
        comp_val = self.components_text.get('1.0', 'end-1c').strip()

        self.current_id = id_val
        self.current_count = count_val
        self.current_components = comp_val

        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_id:
            return ""
        if self.current_components:
            return f'use_remainder={{id:"{self.current_id}",count:{self.current_count},components:{{{self.current_components}}}}}'
        else:
            return f'use_remainder={{id:"{self.current_id}",count:{self.current_count}}}'