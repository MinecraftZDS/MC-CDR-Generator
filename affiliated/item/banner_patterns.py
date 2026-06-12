import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import affiliated.kernel.basic_components as bc

class BannerPatternsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.patterns = []          # 存储字典列表: {"color": str, "pattern": str}
        self.current_index = None

        # 主网格布局
        self.grid_columnconfigure(0, weight=1)  # 左侧列表
        self.grid_columnconfigure(1, weight=2)  # 右侧编辑区
        self.grid_rowconfigure(0, weight=1)

        # ---------- 左侧区域 ----------
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_rowconfigure(0, weight=0)  # 标签
        left_frame.grid_rowconfigure(1, weight=1)  # 列表
        left_frame.grid_rowconfigure(2, weight=0)  # 按钮
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text="Banner Patterns").grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12, width=35)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                                     command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        # ---------- 右侧区域 ----------
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=0)  # 标签
        right_frame.grid_columnconfigure(1, weight=1)  # 输入
        row = 0

        # 红色警告文本
        warning_text = bc.get_lang_text("text.bannerpatterns.warning")
        warning_label = tk.Label(right_frame, text=warning_text, fg="red", wraplength=300, justify='left')
        warning_label.grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        row += 1

        # 颜色下拉
        tk.Label(right_frame, text="Color:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        colors = [
            "white", "orange", "magenta", "light_blue", "yellow",
            "lime", "pink", "gray", "light_gray", "cyan",
            "purple", "blue", "brown", "green", "red", "black"
        ]
        self.color_combo = ttk.Combobox(right_frame, values=colors, state='readonly', width=20)
        self.color_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        if colors:
            self.color_combo.current(0)
        row += 1

        # Pattern 输入框
        tk.Label(right_frame, text="Pattern:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.pattern_entry = tk.Entry(right_frame, width=25)
        self.pattern_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text="Save Pattern",
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 新增按钮单独放在右侧底部（也可放在左侧，但为了方便）
        self.add_btn = ttk.Button(right_frame, text="New Pattern",
                                  command=self._add_new)
        self.add_btn.grid(row=row+1, column=0, columnspan=2, pady=5)

    def _add_new(self):
        """清空表单，进入新增模式"""
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_form()

    def _clear_form(self):
        if self.color_combo['values']:
            self.color_combo.current(0)
        self.pattern_entry.delete(0, tk.END)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        try:
            del self.patterns[self.current_index]
            self._refresh_listbox()
            self.current_index = None
            self._clear_form()
            if self.patterns:
                self.listbox.selection_set(0)
                self._on_select()
            messagebox.showinfo(bc.get_lang_text("deleted.title"),
                                bc.get_lang_text("msg.deleted.modifier"))
        except Exception as e:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("msg.error.failed_delete").format(error=str(e)))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for pat in self.patterns:
            display = f"{pat['color']}: {pat['pattern']}"
            self.listbox.insert(tk.END, display)

    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.current_index = None
            return
        idx = selection[0]
        self.current_index = idx
        pat = self.patterns[idx]
        self.color_combo.set(pat['color'])
        self.pattern_entry.delete(0, tk.END)
        self.pattern_entry.insert(0, pat['pattern'])

    def _save_current(self):
        try:
            color = self.color_combo.get()
            if not color:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     "Color cannot be empty.")
                return
            pattern = self.pattern_entry.get().strip()
            if not pattern:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     "Pattern cannot be empty.")
                return

            # 如果 pattern 不含冒号，自动添加 minecraft: 前缀
            if ':' not in pattern:
                pattern = f"minecraft:{pattern}"

            entry = {
                "color": color,
                "pattern": pattern
            }

            if self.current_index is None:
                self.patterns.append(entry)
                self._refresh_listbox()
                new_idx = len(self.patterns) - 1
                self.listbox.selection_set(new_idx)
                self.current_index = new_idx
            else:
                self.patterns[self.current_index] = entry
                self._refresh_listbox()
                self.listbox.selection_set(self.current_index)

            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(bc.get_lang_text("critical.error.title"),
                                 bc.get_lang_text("msg.error.unexpected").format(error=str(e)))

    def get_nbt(self):
        if not self.patterns:
            return ""
        items = []
        for pat in self.patterns:
            item = f'{{color:"{pat["color"]}",pattern:"{pat["pattern"]}"}}'
            items.append(item)
        return f'banner_patterns=[{",".join(items)}]'