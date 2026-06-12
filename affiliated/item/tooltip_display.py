import tkinter as tk
from tkinter import ttk, messagebox
import json
import affiliated.kernel.basic_components as bc

class TooltipDisplayWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.hide_tooltip = False
        self.hidden_components = []   # 存储字符串列表
        self.current_comp_index = None

        # 布局：左侧列表，右侧编辑区
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- 左侧列表 ----------
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("tooltip_display.components_list")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("tooltip_display.add_component"),
                   command=self._add_component).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_component).pack(side='left', padx=5)

        # ---------- 右侧编辑区 ----------
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        row = 0
        # hide_tooltip 复选框
        self.hide_var = tk.BooleanVar(value=False)
        tk.Checkbutton(right_frame, text=bc.get_lang_text("tooltip_display.hide_tooltip"),
                       variable=self.hide_var).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1

        # 当前组件编辑区
        tk.Label(right_frame, text=bc.get_lang_text("tooltip_display.component_value")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.value_entry = tk.Entry(right_frame, width=40)
        self.value_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("tooltip_display.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 保存顶层按钮
        self.save_top_btn = ttk.Button(right_frame, text=bc.get_lang_text("tooltip_display.save_top"),
                                       command=self._save_top)
        self.save_top_btn.grid(row=row+1, column=0, columnspan=2, pady=10)

        self._refresh_listbox()
        self._add_new()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, comp in enumerate(self.hidden_components):
            self.listbox.insert(tk.END, f"{idx+1}: {comp}")

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_comp_index = None
        self.value_entry.delete(0, tk.END)

    def _add_component(self):
        self.current_comp_index = None
        self.value_entry.delete(0, tk.END)

    def _remove_component(self):
        if self.current_comp_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.hidden_components[self.current_comp_index]
        self._refresh_listbox()
        self.current_comp_index = None
        self.value_entry.delete(0, tk.END)
        if self.hidden_components:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_comp_index = None
            return
        idx = sel[0]
        self.current_comp_index = idx
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, self.hidden_components[idx])

    def _save_current(self):
        val = self.value_entry.get().strip()
        if not val:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("tooltip_display.error.empty"))
            return
        if self.current_comp_index is None:
            self.hidden_components.append(val)
            self._refresh_listbox()
            new_idx = len(self.hidden_components) - 1
            self.listbox.selection_set(new_idx)
            self.current_comp_index = new_idx
        else:
            self.hidden_components[self.current_comp_index] = val
            self._refresh_listbox()
            self.listbox.selection_set(self.current_comp_index)
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def _save_top(self):
        self.hide_tooltip = self.hide_var.get()
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        obj = {"hide_tooltip": self.hide_tooltip}
        if self.hidden_components:
            obj["hidden_components"] = self.hidden_components
        return f'tooltip_display={json.dumps(obj, separators=(",", ":"))}'