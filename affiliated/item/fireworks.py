import tkinter as tk
from tkinter import ttk, messagebox
import json
import traceback
import affiliated.kernel.basic_components as bc

class FireworksWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.flight_duration = 0
        self.explosions = []   # 每个元素是字典

        self.current_index = None

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

        tk.Label(left_frame, text=bc.get_lang_text("fireworks.explosions_list")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("fireworks.add_explosion"),
                   command=self._add_new).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_current).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        row = 0
        # flight_duration
        tk.Label(right_frame, text=bc.get_lang_text("fireworks.flight_duration")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.duration_entry = tk.Entry(right_frame, width=10)
        self.duration_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # 分隔线
        ttk.Separator(right_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
        row += 1

        # 当前爆炸效果编辑区
        self.edit_frame = tk.LabelFrame(right_frame, text=bc.get_lang_text("fireworks.current_explosion"))
        self.edit_frame.grid(row=row, column=0, columnspan=2, sticky='nsew', pady=5)
        right_frame.grid_rowconfigure(row, weight=1)
        row += 1

        # 保存顶层按钮
        self.save_top_btn = ttk.Button(right_frame, text=bc.get_lang_text("fireworks.save_all"),
                                       command=self._save_all)
        self.save_top_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 初始化
        self._refresh_listbox()
        self._add_new()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, exp in enumerate(self.explosions):
            shape = exp.get('shape', '?')
            self.listbox.insert(tk.END, f"{idx+1}: {shape}")

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_edit_form()

    def _clear_edit_form(self):
        for w in self.edit_frame.winfo_children():
            w.destroy()
        self._build_edit_ui()

    def _build_edit_ui(self):
        self.edit_colors_entry = tk.Entry(self.edit_frame, width=10)
        self.edit_trail_var = tk.BooleanVar()
        self.edit_twinkle_var = tk.BooleanVar()
        shapes = ["small_ball", "large_ball", "star", "creeper", "burst"]
        self.edit_shape_combo = ttk.Combobox(self.edit_frame, values=shapes, state='readonly', width=15)

        row = 0
        tk.Label(self.edit_frame, text=bc.get_lang_text("firework.colors")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.edit_colors_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        tk.Checkbutton(self.edit_frame, text=bc.get_lang_text("firework.has_trail"),
                       variable=self.edit_trail_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1
        tk.Checkbutton(self.edit_frame, text=bc.get_lang_text("firework.has_twinkle"),
                       variable=self.edit_twinkle_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1
        tk.Label(self.edit_frame, text=bc.get_lang_text("firework.shape")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.edit_shape_combo.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        self.edit_shape_combo.current(0)
        row += 1

        save_btn = ttk.Button(self.edit_frame, text=bc.get_lang_text("fireworks.save_explosion"),
                              command=self._save_current_explosion)
        save_btn.grid(row=row, column=0, columnspan=2, pady=10)

    def _save_current_explosion(self):
        try:
            colors = int(self.edit_colors_entry.get().strip() or "0")
        except:
            colors = 0
        trail = self.edit_trail_var.get()
        twinkle = self.edit_twinkle_var.get()
        shape = self.edit_shape_combo.get()
        if shape not in ["small_ball", "large_ball", "star", "creeper", "burst"]:
            shape = "small_ball"

        explosion = {
            "colors": [colors],
            "has_trail": trail,
            "has_twinkle": twinkle,
            "shape": shape
        }

        if self.current_index is None:
            self.explosions.append(explosion)
            self._refresh_listbox()
            self.listbox.selection_set(len(self.explosions)-1)
            self.current_index = len(self.explosions)-1
        else:
            self.explosions[self.current_index] = explosion
            self._refresh_listbox()
            self.listbox.selection_set(self.current_index)
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.explosions[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self._clear_edit_form()
        if self.explosions:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            self._clear_edit_form()
            return
        idx = sel[0]
        self.current_index = idx
        exp = self.explosions[idx]
        self._clear_edit_form()
        self.edit_colors_entry.insert(0, str(exp.get('colors', [0])[0]))
        self.edit_trail_var.set(exp.get('has_trail', False))
        self.edit_twinkle_var.set(exp.get('has_twinkle', False))
        self.edit_shape_combo.set(exp.get('shape', 'small_ball'))

    def _save_all(self):
        try:
            duration = int(self.duration_entry.get().strip() or "0")
            if duration < 0:
                raise ValueError
            self.flight_duration = duration
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("fireworks.error.flight_duration"))

    def get_nbt(self):
        if not self.explosions and self.flight_duration == 0:
            return ""
        explosions_list = []
        for exp in self.explosions:
            obj = {
                "colors": exp["colors"],
                "has_trail": exp["has_trail"],
                "has_twinkle": exp["has_twinkle"],
                "shape": exp["shape"]
            }
            explosions_list.append(obj)
        top = {
            "flight_duration": self.flight_duration,
            "explosions": explosions_list
        }
        nbt_str = json.dumps(top, separators=(',', ':'))
        return f'fireworks={nbt_str}'