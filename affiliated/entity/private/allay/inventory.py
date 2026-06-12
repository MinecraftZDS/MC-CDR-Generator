import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import traceback
import affiliated.kernel.basic_components as bc

class InventoryWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_id = ""
        self.current_components = ""
        self.current_count = 1

        # 使用可滚动区域
        canvas = tk.Canvas(self, highlightthickness=0)
        v_scroll = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        h_scroll = tk.Scrollbar(self, orient='horizontal', command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))

        # 物品 ID
        tk.Label(inner, text=bc.get_lang_text("inventory.id_label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.id_entry = tk.Entry(inner, width=40)
        self.id_entry.pack(fill='x', padx=5, pady=2)

        # 数量
        tk.Label(inner, text=bc.get_lang_text("inventory.count_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.count_entry = tk.Entry(inner, width=10)
        self.count_entry.pack(anchor='w', padx=5, pady=2)
        self.count_entry.insert(0, "1")

        # 组件
        tk.Label(inner, text=bc.get_lang_text("inventory.components_label")).pack(anchor='w', padx=5, pady=(5, 0))
        self.components_text = ScrolledText(inner, height=6, wrap='word', font=('Consolas', 10))
        self.components_text.pack(fill='both', expand=True, padx=5, pady=5)

        # 保存按钮
        self.save_btn = ttk.Button(inner, text=bc.get_lang_text("inventory.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        id_val = self.id_entry.get().strip()
        if not id_val:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("inventory.error.id_empty"))
            return
        try:
            count_val = int(self.count_entry.get().strip())
            if count_val < 0:
                raise ValueError
            if count_val > 1:
                count_val = 1
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("inventory.error.count_invalid"))
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
        item_obj = {"id": self.current_id, "count": self.current_count}
        if self.current_components:
            comp_str = self.current_components.strip()
            if not comp_str.startswith('{'):
                comp_str = '{' + comp_str + '}'
            try:
                item_obj["components"] = json.loads(comp_str)
            except:
                item_obj["components"] = comp_str
        # Inventory 是数组，包含一个元素
        return f'Inventory:[{json.dumps(item_obj, separators=(",", ":"))}]'