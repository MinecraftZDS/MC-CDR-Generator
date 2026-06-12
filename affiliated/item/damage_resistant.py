import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import affiliated.kernel.basic_components as bc

class DamageResistantWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.items = []   # 存储 damage_type 字符串
        self.current_index = None

        # 加载预设伤害类型列表
        self.damage_types_presets = self._load_damage_types()

        # 布局
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 左侧列表
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("damage_resistant.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("damage_resistant.add"),
                   command=self._add_new).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_current).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        # 下拉选择预设 + 手动输入
        tk.Label(right_frame, text=bc.get_lang_text("damage_resistant.type_label")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.type_combo = ttk.Combobox(right_frame, values=self.damage_types_presets, width=30)
        self.type_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.type_combo.bind('<Return>', lambda e: self._save_current())  # 回车保存

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("damage_resistant.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self._add_new()

    def _load_damage_types(self):
        """从 affiliated/lists.json 读取 damage_types 列表"""
        base_dir = os.path.dirname(os.path.dirname(__file__))  # affiliated 目录
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('damage_types', [])
        except:
            return []

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self.type_combo.set('')

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.items[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self.type_combo.set('')
        if self.items:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, val in enumerate(self.items):
            self.listbox.insert(tk.END, f"{idx+1}: {val}")

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        self.type_combo.set(self.items[idx])

    def _save_current(self):
        val = self.type_combo.get().strip()
        if not val:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("damage_resistant.error.empty"))
            return
        if self.current_index is None:
            self.items.append(val)
            self._refresh_listbox()
            new_idx = len(self.items) - 1
            self.listbox.selection_set(new_idx)
            self.current_index = new_idx
        else:
            self.items[self.current_index] = val
            self._refresh_listbox()
            self.listbox.selection_set(self.current_index)
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.items:
            return ""
        items_json = ','.join(f'"{item}"' for item in self.items)
        return f'damage_resistant={{types:[{items_json}]}}'