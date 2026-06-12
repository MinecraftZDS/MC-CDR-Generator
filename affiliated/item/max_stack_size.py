import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class MaxStackSizeWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_size = 1

        tk.Label(self, text=bc.get_lang_text("max_stack_size.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.size_entry = tk.Entry(self, width=10)
        self.size_entry.pack(anchor='w', padx=5, pady=2)
        self.size_entry.insert(0, "")

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("max_stack_size.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            val = int(self.size_entry.get().strip())
            if val < 0 or val > 99:
                raise ValueError
            self.current_size = val
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("max_stack_size.error.invalid"))

    def get_nbt(self):
        # 仅当不为默认值1时输出，或者总是输出？按需求输出即可
        # 默认值1可以省略，但为保险，总是输出
        return f'max_stack_size={self.current_size}'