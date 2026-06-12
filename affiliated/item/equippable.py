import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import affiliated.kernel.basic_components as bc

class EquippableWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 存储数据
        self.allowed_entities = []  # 实体ID列表
        self.asset_id = ""
        self.camera_overlay = ""
        self.damage_on_hurt = False
        self.equip_on_sheared = False
        self.dispensable = False
        self.slot = "any"
        self.swappable = False

        # 布局使用 grid
        self.grid_columnconfigure(1, weight=1)

        row = 0

        # allowed_entities（独立窗口）
        tk.Label(self, text=bc.get_lang_text("equippable.allowed_entities_label")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.allowed_btn = ttk.Button(self, text=bc.get_lang_text("equippable.manage_entities"),
                                      command=self._manage_allowed_entities)
        self.allowed_btn.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # asset_id (可选字符串)
        tk.Label(self, text=bc.get_lang_text("equippable.asset_id")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.asset_entry = tk.Entry(self, width=30)
        self.asset_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # camera_overlay (可选字符串)
        tk.Label(self, text=bc.get_lang_text("equippable.camera_overlay")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.camera_entry = tk.Entry(self, width=30)
        self.camera_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # damage_on_hurt (布尔)
        self.damage_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("equippable.damage_on_hurt"),
                       variable=self.damage_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # equip_on_sheared
        self.shear_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("equippable.equip_on_sheared"),
                       variable=self.shear_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # dispensable
        self.disp_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("equippable.dispensable"),
                       variable=self.disp_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # slot (下拉)
        tk.Label(self, text=bc.get_lang_text("equippable.slot")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        slot_values = [
            "head", "chest", "legs", "feet", "any",
            "mainhand", "offhand", "body", "saddle"
        ]
        self.slot_combo = ttk.Combobox(self, values=slot_values, state='readonly', width=15)
        self.slot_combo.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        self.slot_combo.current(4)  # "any"
        row += 1

        # swappable
        self.swap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("equippable.swappable"),
                       variable=self.swap_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("equippable.save"),
                                   command=self._save)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 静默初始化
        self._save(silent=True)

    def _manage_allowed_entities(self):
        """打开二级窗口管理 allowed_entities 列表"""
        win = tk.Toplevel(self)
        win.title(bc.get_lang_text("equippable.entities_window_title"))
        win.geometry("500x400")
        win.transient(self)
        win.grab_set()

        frame = tk.Frame(win)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(frame, text=bc.get_lang_text("equippable.entities_list")).pack(anchor='w')
        listbox = tk.Listbox(frame, height=12)
        listbox.pack(fill='both', expand=True, pady=5)

        def refresh():
            listbox.delete(0, tk.END)
            for eid in self.allowed_entities:
                listbox.insert(tk.END, eid)

        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill='x', pady=5)
        tk.Label(entry_frame, text=bc.get_lang_text("equippable.entity_id")).pack(side='left', padx=5)
        entry = tk.Entry(entry_frame, width=30)
        entry.pack(side='left', padx=5)
        def add():
            val = entry.get().strip()
            if val and val not in self.allowed_entities:
                self.allowed_entities.append(val)
                refresh()
                entry.delete(0, tk.END)
        ttk.Button(entry_frame, text=bc.get_lang_text("equippable.add_entity"), command=add).pack(side='left')

        def remove():
            sel = listbox.curselection()
            if sel:
                del self.allowed_entities[sel[0]]
                refresh()
        ttk.Button(frame, text=bc.get_lang_text("button.remove_modifier"), command=remove).pack(pady=5)

        refresh()
        # 当窗口关闭时，自动保存（不额外弹窗，因为用户已在主窗口保存）
        # 但主窗口保存时会读取 self.allowed_entities

    def _save(self, silent=False):
        # 收集数据
        self.allowed_entities = self.allowed_entities  # 已通过二级窗口更新
        self.asset_id = self.asset_entry.get().strip()
        self.camera_overlay = self.camera_entry.get().strip()
        self.damage_on_hurt = self.damage_var.get()
        self.equip_on_sheared = self.shear_var.get()
        self.dispensable = self.disp_var.get()
        self.slot = self.slot_combo.get().strip()
        self.swappable = self.swap_var.get()

        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        # 构建 NBT 对象
        obj = {}
        if self.allowed_entities:
            obj["allowed_entities"] = self.allowed_entities
        if self.asset_id:
            obj["asset_id"] = self.asset_id
        if self.camera_overlay:
            obj["camera_overlay"] = self.camera_overlay
        obj["damage_on_hurt"] = self.damage_on_hurt
        obj["equip_on_sheared"] = self.equip_on_sheared
        obj["dispensable"] = self.dispensable
        obj["slot"] = self.slot
        obj["swappable"] = self.swappable

        # 使用 json 序列化为对象字符串
        obj_str = json.dumps(obj, separators=(',', ':'))
        return f'equippable={obj_str}'