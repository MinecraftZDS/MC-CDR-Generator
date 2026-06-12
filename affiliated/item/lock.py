import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import traceback
import affiliated.kernel.basic_components as bc

class LockWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 数据存储
        self.components_text = ""
        self.count_min = 0
        self.count_max = 0
        self.items_list = []

        # 使用 grid 布局，设置权重
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # components 区域可伸缩
        self.grid_rowconfigure(2, weight=1)  # items 区域可伸缩

        row = 0
        # components 标签和文本框
        tk.Label(self, text=bc.get_lang_text("lock.components_label")).grid(row=row, column=0, sticky='nw', padx=5, pady=2)
        self.components_text_widget = ScrolledText(self, height=6, wrap='word', font=('Consolas', 10))
        self.components_text_widget.grid(row=row, column=1, sticky='nsew', padx=5, pady=2)
        row += 1

        # count 区域
        count_frame = tk.LabelFrame(self, text=bc.get_lang_text("lock.count_group"))
        count_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        count_frame.columnconfigure(1, weight=1)
        # min
        tk.Label(count_frame, text=bc.get_lang_text("lock.count_min")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.min_entry = tk.Entry(count_frame, width=5)
        self.min_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.min_entry.insert(0, "0")
        # max
        tk.Label(count_frame, text=bc.get_lang_text("lock.count_max")).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.max_entry = tk.Entry(count_frame, width=5)
        self.max_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.max_entry.insert(0, "0")
        row += 1

        # items 列表管理
        items_frame = tk.LabelFrame(self, text=bc.get_lang_text("lock.items_group"))
        items_frame.grid(row=row, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        items_frame.grid_rowconfigure(1, weight=1)
        items_frame.grid_columnconfigure(0, weight=1)

        tk.Label(items_frame, text=bc.get_lang_text("lock.items_list")).grid(row=0, column=0, sticky='w', padx=5)
        self.items_listbox = tk.Listbox(items_frame, height=6)
        self.items_listbox.grid(row=1, column=0, sticky='nsew', pady=5, padx=5)
        self.items_listbox.bind('<<ListboxSelect>>', self._on_item_select)

        # 添加/删除按钮
        btn_frame = tk.Frame(items_frame)
        btn_frame.grid(row=2, column=0, pady=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("lock.add_item"),
                   command=self._add_item_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_item).pack(side='left', padx=5)
        row += 1

        # 单独保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("lock.save"),
                                   command=self._save)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        self._save(silent=True)

    def _add_item_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title(bc.get_lang_text("lock.add_item_title"))
        dialog.geometry("300x120")
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text=bc.get_lang_text("lock.item_id")).pack(padx=5, pady=5)
        entry = tk.Entry(dialog, width=30)
        entry.pack(padx=5, pady=5)

        def confirm():
            val = entry.get().strip()
            if val:
                if val not in self.items_list:
                    self.items_list.append(val)
                    self._refresh_items_list()
                else:
                    messagebox.showwarning(bc.get_lang_text("warning.title"),
                                           bc.get_lang_text("lock.item_duplicate"))
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=confirm).pack(pady=5)

    def _remove_item(self):
        sel = self.items_listbox.curselection()
        if sel:
            idx = sel[0]
            del self.items_list[idx]
            self._refresh_items_list()

    def _refresh_items_list(self):
        self.items_listbox.delete(0, tk.END)
        for item in self.items_list:
            self.items_listbox.insert(tk.END, item)

    def _on_item_select(self, event=None):
        # 仅用于显示选中，不需要额外操作
        pass

    def _save(self, silent=False):
        try:
            # 收集 components
            comp_text = self.components_text_widget.get('1.0', 'end-1c').strip()
            self.components_text = comp_text

            # 收集 count
            min_val = int(self.min_entry.get().strip() or "0")
            max_val = int(self.max_entry.get().strip() or "0")
            if not (0 <= min_val <= 99 and 0 <= max_val <= 99):
                raise ValueError("Count values must be between 0 and 99")
            self.count_min = min_val
            self.count_max = max_val

            # items 已通过列表存储
            # 无额外验证，物品 ID 可以是任意字符串

            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except ValueError as e:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"), str(e))
        except Exception as e:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("lock.error.general").format(error=str(e)))

    def get_nbt(self):
        # 构建 NBT 对象
        obj = {}
        if self.components_text:
            # 注意：components 字段的值是一个对象，用户输入的内容应被当作对象插入，不需要额外花括号
            # 我们直接拼接 components:{用户输入}，但用户输入必须已经是有效的 NBT 对象字符串（如 {ench:...}）
            # 为了安全，我们允许用户输入不带花括号的键值对？这里按用户输入原样插入。
            # 假设用户输入的是花括号内的内容，我们补上花括号；如果用户已经包含花括号，则直接使用。
            comp = self.components_text.strip()
            if not comp.startswith('{'):
                comp = f'{{{comp}}}'
            obj["components"] = json.loads(comp)  # 尝试解析为 JSON 对象
        if self.count_min != 0 or self.count_max != 0:
            obj["count"] = {"min": self.count_min, "max": self.count_max}
        if self.items_list:
            obj["items"] = self.items_list

        if not obj:
            return ""
        return f'lock={json.dumps(obj, separators=(",", ":"))}'