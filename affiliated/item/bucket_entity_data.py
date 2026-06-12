import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import affiliated.kernel.basic_components as bc

class BucketEntityDataWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)
        self.current_data = ""

        tk.Label(self, text=bc.get_lang_text("bucket_entity_data.label")).pack(anchor='w', padx=5, pady=(10,0))
        self.text_area = ScrolledText(self, height=8, wrap='word', font=('Consolas',10))
        self.text_area.pack(fill='both', expand=True, padx=5, pady=5)
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("bucket_entity_data.save"), command=self._save)
        self.save_btn.pack(pady=10)
        self._save(silent=True)

    def _save(self, silent=False):
        data = self.text_area.get('1.0', 'end-1c').strip()
        self.current_data = data
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        return f'bucket_entity_data={{{self.current_data}}}' if self.current_data else ""