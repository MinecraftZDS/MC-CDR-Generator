import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os
import traceback
import affiliated.kernel.basic_components as bc

class PotionContentsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 数据存储
        self.custom_color = None   # None 表示未设置
        self.potion = ""           # 药水 ID
        self.custom_effects = []   # 子效果列表

        self.current_effect_index = None

        # 加载药水效果列表
        self.potion_effects = self._load_potion_effects()

        # 布局：左侧列表，右侧编辑区
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 左侧列表
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("potion_contents.effects_list")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("potion_contents.add_effect"),
                   command=self._add_effect).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_effect).pack(side='left', padx=5)

        # 右侧编辑区（顶层：颜色 + 药水ID + 滚动区域）
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        # 固定顶栏：自定义颜色和药水ID
        row = 0
        tk.Label(right_frame, text=bc.get_lang_text("potion_contents.custom_color")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.color_entry = tk.Entry(right_frame, width=10)
        self.color_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        tk.Label(right_frame, text=bc.get_lang_text("potion_contents.potion")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.potion_entry = tk.Entry(right_frame, width=40)
        self.potion_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # 效果编辑区域（可滚动）
        canvas_frame = tk.Frame(right_frame)
        canvas_frame.grid(row=row, column=0, columnspan=2, sticky='nsew', pady=5)
        right_frame.grid_rowconfigure(row, weight=1)
        row += 1

        canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self.effect_inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.effect_inner, anchor='nw', width=canvas.winfo_reqwidth())

        def _on_inner_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        self.effect_inner.bind('<Configure>', _on_inner_configure)

        def _on_canvas_configure(event):
            canvas.itemconfig(1, width=event.width)
        canvas.bind('<Configure>', _on_canvas_configure)

        # 在 effect_inner 中构建效果编辑表单
        self._build_effect_form()

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("potion_contents.save"),
                                   command=self._save_all)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        self._refresh_listbox()
        self._clear_effect_form()

    def _load_potion_effects(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('potion_effects', [])
        except:
            return []

    # ---------- 左侧效果列表管理 ----------
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, eff in enumerate(self.custom_effects):
            eff_id = eff.get('id', '?')
            amp = eff.get('amplifier', 0)
            dur = eff.get('duration', 0)
            self.listbox.insert(tk.END, f"{idx+1}: {eff_id} amp:{amp} dur:{dur}")

    def _add_effect(self):
        self.current_effect_index = None
        self._clear_effect_form()

    def _remove_effect(self):
        if self.current_effect_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.custom_effects[self.current_effect_index]
        self.current_effect_index = None
        self._refresh_listbox()
        self._clear_effect_form()
        if self.custom_effects:
            self.listbox.selection_set(0)
            self._on_select()

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_effect_index = None
            self._clear_effect_form()
            return
        idx = sel[0]
        self.current_effect_index = idx
        effect = self.custom_effects[idx]
        self._load_effect_to_form(effect)

    # ---------- 右侧效果编辑表单 ----------
    def _clear_effect_form(self):
        # 清空所有输入控件
        if hasattr(self, 'id_combo'):
            self.id_combo.set('')
        if hasattr(self, 'duration_entry'):
            self.duration_entry.delete(0, tk.END)
        if hasattr(self, 'amplifier_entry'):
            self.amplifier_entry.delete(0, tk.END)
        if hasattr(self, 'ambient_var'):
            self.ambient_var.set(False)
        if hasattr(self, 'show_icon_var'):
            self.show_icon_var.set(True)
        if hasattr(self, 'show_particles_var'):
            self.show_particles_var.set(True)

    def _build_effect_form(self):
        # 创建表单控件（放在 self.effect_inner 中）
        self.effect_fields = {}
        row = 0
        # id 下拉框
        tk.Label(self.effect_inner, text="id").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.id_combo = ttk.Combobox(self.effect_inner, values=self.potion_effects, state='readonly', width=30)
        self.id_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # duration
        tk.Label(self.effect_inner, text="duration").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.duration_entry = tk.Entry(self.effect_inner, width=10)
        self.duration_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # amplifier
        tk.Label(self.effect_inner, text="amplifier").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.amplifier_entry = tk.Entry(self.effect_inner, width=10)
        self.amplifier_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # ambient
        self.ambient_var = tk.BooleanVar()
        tk.Checkbutton(self.effect_inner, text="ambient", variable=self.ambient_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # show_icon
        self.show_icon_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.effect_inner, text="show_icon", variable=self.show_icon_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # show_particles
        self.show_particles_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.effect_inner, text="show_particles", variable=self.show_particles_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # 保存当前效果按钮
        self.save_effect_btn = ttk.Button(self.effect_inner, text=bc.get_lang_text("potion_contents.save_effect"),
                                          command=self._save_current_effect)
        self.save_effect_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 让 effect_inner 的列可伸缩
        self.effect_inner.columnconfigure(1, weight=1)

    def _load_effect_to_form(self, effect):
        self._clear_effect_form()
        # 填充数据
        self.id_combo.set(effect.get('id', ''))
        self.duration_entry.insert(0, str(effect.get('duration', 0)))
        self.amplifier_entry.insert(0, str(effect.get('amplifier', 0)))
        self.ambient_var.set(effect.get('ambient', False))
        self.show_icon_var.set(effect.get('show_icon', True))
        self.show_particles_var.set(effect.get('show_particles', True))

    def _save_current_effect(self):
        try:
            effect_id = self.id_combo.get().strip()
            if not effect_id:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("potion_contents.error.no_effect_id"))
                return
            duration = int(self.duration_entry.get().strip() or "0")
            if duration < 0:
                raise ValueError
            amplifier = int(self.amplifier_entry.get().strip() or "0")
            if amplifier < 0:
                raise ValueError
            ambient = self.ambient_var.get()
            show_icon = self.show_icon_var.get()
            show_particles = self.show_particles_var.get()

            new_effect = {
                "id": effect_id,
                "duration": duration,
                "amplifier": amplifier,
                "ambient": ambient,
                "show_icon": show_icon,
                "show_particles": show_particles
            }

            if self.current_effect_index is None:
                self.custom_effects.append(new_effect)
            else:
                self.custom_effects[self.current_effect_index] = new_effect
            self._refresh_listbox()
            self.current_effect_index = None
            self._clear_effect_form()
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("potion_contents.error.invalid_number"))

    # ---------- 顶层保存 ----------
    def _save_all(self):
        try:
            custom_color_str = self.color_entry.get().strip()
            custom_color = None
            if custom_color_str:
                val = int(custom_color_str)
                if 0 <= val <= 16777215:
                    custom_color = val
                else:
                    raise ValueError
            self.custom_color = custom_color
            self.potion = self.potion_entry.get().strip()
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("potion_contents.error.invalid_color"))

    # ---------- NBT 生成 ----------
    def get_nbt(self):
        obj = {}
        if self.custom_color is not None:
            obj["custom_color"] = self.custom_color
        if self.potion:
            obj["potion"] = self.potion
        if self.custom_effects:
            obj["custom_effects"] = self.custom_effects

        if not obj:
            return ""
        return f'potion_contents={json.dumps(obj, separators=(",", ":"))}'