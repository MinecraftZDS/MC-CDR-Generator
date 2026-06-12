import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import traceback
import affiliated.kernel.basic_components as bc

class EnchantmentsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.enchantments = {}   # 字典: {id: level}
        self.current_key = None

        # 加载附魔列表
        self.enchant_list = self._load_enchantments()

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

        tk.Label(left_frame, text=bc.get_lang_text("enchantments.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("enchantments.add"),
                   command=self._add_new).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_current).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        # 附魔下拉
        tk.Label(right_frame, text=bc.get_lang_text("enchantments.enchant")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.enchant_combo = ttk.Combobox(right_frame, values=self.enchant_list, state='readonly', width=30)
        self.enchant_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # 等级输入
        tk.Label(right_frame, text=bc.get_lang_text("enchantments.level")).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.level_entry = tk.Entry(right_frame, width=10)
        self.level_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("enchantments.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self._refresh_listbox()
        self._add_new()

    def _load_enchantments(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('enchantments', [])
        except:
            return []

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, (eid, lvl) in enumerate(self.enchantments.items()):
            self.listbox.insert(tk.END, f"{idx+1}: {eid} lv{lvl}")

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_key = None
        self.enchant_combo.set('')
        self.level_entry.delete(0, tk.END)

    def _remove_current(self):
        if self.current_key is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.enchantments[self.current_key]
        self._refresh_listbox()
        self.current_key = None
        self.enchant_combo.set('')
        self.level_entry.delete(0, tk.END)
        if self.enchantments:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_key = None
            return
        idx = sel[0]
        key = list(self.enchantments.keys())[idx]
        self.current_key = key
        self.enchant_combo.set(key)
        self.level_entry.delete(0, tk.END)
        self.level_entry.insert(0, str(self.enchantments[key]))

    def _save_current(self):
        ench = self.enchant_combo.get().strip()
        if not ench:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("enchantments.error.no_enchant"))
            return
        try:
            lvl = int(self.level_entry.get().strip())
            if lvl < 1:
                raise ValueError
        except:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("enchantments.error.invalid_level"))
            return

        if self.current_key is None:
            if ench in self.enchantments:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("enchantments.error.duplicate"))
                return
            self.enchantments[ench] = lvl
            self._refresh_listbox()
            self.listbox.selection_set(len(self.enchantments)-1)
            self.current_key = ench
        else:
            if ench != self.current_key and ench in self.enchantments:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("enchantments.error.duplicate"))
                return
            del self.enchantments[self.current_key]
            self.enchantments[ench] = lvl
            self._refresh_listbox()
            # 找到新键的索引
            new_idx = list(self.enchantments.keys()).index(ench)
            self.listbox.selection_set(new_idx)
            self.current_key = ench
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.enchantments:
            return ""
        # 生成 JSON 对象字符串，例如 {"minecraft:sharpness":5}
        obj_str = json.dumps(self.enchantments, separators=(',', ':'))
        return f'enchantments={obj_str}'