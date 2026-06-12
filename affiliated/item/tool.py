import tkinter as tk
from tkinter import ttk, messagebox
import json
import traceback
import affiliated.kernel.basic_components as bc

class ToolWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 数据存储
        self.can_destroy_creative = False
        self.damage_per_block = 0
        self.default_mining_speed = 0.0
        self.rules = []
        self.current_rule_index = None

        # 布局：左右分栏
        self.grid_columnconfigure(0, weight=0)   # 左侧固定宽度
        self.grid_columnconfigure(1, weight=1)   # 右侧伸缩
        self.grid_rowconfigure(0, weight=1)

        # ---------- 左侧：规则列表 ----------
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("tool.rules_list")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("tool.add_rule"),
                   command=self._add_rule).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_rule).pack(side='left', padx=5)

        # ---------- 右侧：可滚动区域 ----------
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # 创建画布和滚动条
        canvas = tk.Canvas(right_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(right_frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self.inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        def _on_inner_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        self.inner_frame.bind('<Configure>', _on_inner_configure)

        def _on_canvas_configure(event):
            canvas.itemconfig(1, width=event.width)
        canvas.bind('<Configure>', _on_canvas_configure)

        # ---------- 在 inner_frame 中放置所有编辑控件 ----------
        # 顶层字段
        self.creative_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.inner_frame, text=bc.get_lang_text("tool.can_destroy_creative"),
                       variable=self.creative_var).pack(anchor='w', padx=5, pady=2)

        tk.Label(self.inner_frame, text=bc.get_lang_text("tool.damage_per_block")).pack(anchor='w', padx=5, pady=2)
        self.damage_entry = tk.Entry(self.inner_frame, width=10)
        self.damage_entry.pack(anchor='w', padx=5, pady=2)

        tk.Label(self.inner_frame, text=bc.get_lang_text("tool.default_mining_speed")).pack(anchor='w', padx=5, pady=2)
        self.speed_entry = tk.Entry(self.inner_frame, width=10)
        self.speed_entry.pack(anchor='w', padx=5, pady=2)

        # 规则编辑区域（标签框架）
        rule_frame = tk.LabelFrame(self.inner_frame, text=bc.get_lang_text("tool.current_rule"))
        rule_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # blocks 列表管理
        tk.Label(rule_frame, text=bc.get_lang_text("tool.blocks_list")).pack(anchor='w', padx=5, pady=(5,0))
        listbox_frame = tk.Frame(rule_frame)
        listbox_frame.pack(fill='x', padx=5, pady=2)
        self.blocks_listbox = tk.Listbox(listbox_frame, height=4, width=30)
        self.blocks_listbox.pack(side='left', fill='both', expand=True)
        scroll2 = tk.Scrollbar(listbox_frame, orient='vertical', command=self.blocks_listbox.yview)
        scroll2.pack(side='right', fill='y')
        self.blocks_listbox.config(yscrollcommand=scroll2.set)

        blocks_btn_frame = tk.Frame(rule_frame)
        blocks_btn_frame.pack(fill='x', padx=5, pady=2)
        ttk.Button(blocks_btn_frame, text=bc.get_lang_text("tool.add_block"),
                   command=self._add_block).pack(side='left', padx=2)
        ttk.Button(blocks_btn_frame, text=bc.get_lang_text("tool.edit_block"),
                   command=self._edit_block).pack(side='left', padx=2)
        ttk.Button(blocks_btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_block).pack(side='left', padx=2)

        # correct_for_drops
        self.correct_var = tk.BooleanVar(value=False)
        tk.Checkbutton(rule_frame, text=bc.get_lang_text("tool.correct_for_drops"),
                       variable=self.correct_var).pack(anchor='w', padx=5, pady=2)

        # speed
        tk.Label(rule_frame, text=bc.get_lang_text("tool.rule_speed")).pack(anchor='w', padx=5, pady=2)
        self.rule_speed_entry = tk.Entry(rule_frame, width=10)
        self.rule_speed_entry.pack(anchor='w', padx=5, pady=2)

        # 保存当前规则按钮
        self.save_rule_btn = ttk.Button(rule_frame, text=bc.get_lang_text("tool.save_rule"),
                                        command=self._save_current_rule)
        self.save_rule_btn.pack(pady=5)

        # 保存顶层按钮
        self.save_top_btn = ttk.Button(self.inner_frame, text=bc.get_lang_text("tool.save_top"),
                                       command=self._save_top)
        self.save_top_btn.pack(pady=10)

        # 初始化
        self.blocks_list = []
        self._refresh_blocks_listbox()
        self._refresh_listbox()
        self._clear_rule_form()

    # ---------- 辅助方法 ----------
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, rule in enumerate(self.rules):
            blocks_preview = ", ".join(rule['blocks'][:2])
            if len(rule['blocks']) > 2:
                blocks_preview += "..."
            self.listbox.insert(tk.END, f"{idx+1}: [{blocks_preview}] speed:{rule['speed']}")

    def _add_rule(self):
        self.current_rule_index = None
        self._clear_rule_form()

    def _clear_rule_form(self):
        self.blocks_list = []
        self._refresh_blocks_listbox()
        self.correct_var.set(False)
        self.rule_speed_entry.delete(0, tk.END)
        self.rule_speed_entry.insert(0, "0.0")

    def _remove_rule(self):
        if self.current_rule_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.rules[self.current_rule_index]
        self.current_rule_index = None
        self._refresh_listbox()
        self._clear_rule_form()
        if self.rules:
            self.listbox.selection_set(0)
            self._on_select()

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_rule_index = None
            return
        idx = sel[0]
        self.current_rule_index = idx
        rule = self.rules[idx]
        self.blocks_list = rule['blocks'][:]
        self._refresh_blocks_listbox()
        self.correct_var.set(rule['correct_for_drops'])
        self.rule_speed_entry.delete(0, tk.END)
        self.rule_speed_entry.insert(0, str(rule['speed']))

    def _save_current_rule(self):
        try:
            blocks = self.blocks_list[:]
            if not blocks:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("tool.error.no_blocks"))
                return
            correct = self.correct_var.get()
            speed_str = self.rule_speed_entry.get().strip()
            speed = float(speed_str) if speed_str else 0.0
            if speed < 0:
                raise ValueError
            rule = {
                "blocks": blocks,
                "correct_for_drops": correct,
                "speed": speed
            }
            if self.current_rule_index is None:
                self.rules.append(rule)
            else:
                self.rules[self.current_rule_index] = rule
            self._refresh_listbox()
            self.current_rule_index = None
            self._clear_rule_form()
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("tool.error.invalid_speed"))

    def _save_top(self):
        try:
            self.can_destroy_creative = self.creative_var.get()
            damage_str = self.damage_entry.get().strip()
            self.damage_per_block = int(damage_str) if damage_str else 0
            if self.damage_per_block < 0:
                raise ValueError
            speed_str = self.speed_entry.get().strip()
            self.default_mining_speed = float(speed_str) if speed_str else 0.0
            if self.default_mining_speed < 0:
                raise ValueError
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("tool.error.top_invalid"))

    # ---------- blocks 列表管理 ----------
    def _refresh_blocks_listbox(self):
        self.blocks_listbox.delete(0, tk.END)
        for b in self.blocks_list:
            self.blocks_listbox.insert(tk.END, b)

    def _add_block(self):
        dialog = tk.Toplevel(self)
        dialog.title(bc.get_lang_text("tool.add_block_title"))
        dialog.geometry("300x120")
        dialog.transient(self)
        dialog.grab_set()
        tk.Label(dialog, text=bc.get_lang_text("tool.block_id")).pack(padx=5, pady=5)
        entry = tk.Entry(dialog, width=30)
        entry.pack(padx=5, pady=5)
        def confirm():
            val = entry.get().strip()
            if val:
                self.blocks_list.append(val)
                self._refresh_blocks_listbox()
            dialog.destroy()
        ttk.Button(dialog, text="OK", command=confirm).pack(pady=5)

    def _edit_block(self):
        sel = self.blocks_listbox.curselection()
        if not sel:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("tool.error.no_block_selected"))
            return
        idx = sel[0]
        current_block = self.blocks_list[idx]
        dialog = tk.Toplevel(self)
        dialog.title(bc.get_lang_text("tool.edit_block_title"))
        dialog.geometry("300x120")
        dialog.transient(self)
        dialog.grab_set()
        tk.Label(dialog, text=bc.get_lang_text("tool.block_id")).pack(padx=5, pady=5)
        entry = tk.Entry(dialog, width=30)
        entry.pack(padx=5, pady=5)
        entry.insert(0, current_block)
        def confirm():
            new_val = entry.get().strip()
            if new_val:
                self.blocks_list[idx] = new_val
                self._refresh_blocks_listbox()
            dialog.destroy()
        ttk.Button(dialog, text="OK", command=confirm).pack(pady=5)

    def _remove_block(self):
        sel = self.blocks_listbox.curselection()
        if sel:
            del self.blocks_list[sel[0]]
            self._refresh_blocks_listbox()

    def get_nbt(self):
        obj = {
            "can_destroy_blocks_in_creative": self.can_destroy_creative,
            "damage_per_block": self.damage_per_block,
            "default_mining_speed": self.default_mining_speed,
            "rules": self.rules
        }
        if not obj["rules"]:
            del obj["rules"]
        return f'tool={json.dumps(obj, separators=(",", ":"))}'