import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import traceback
import affiliated.kernel.basic_components as bc

class BeesWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.bees = []          # 每个元素: {"min_ticks": int, "ticks": int, "entity_data": str}
        self.current_index = None

        # 主网格布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # 左侧区域
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_rowconfigure(0, weight=0)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_rowconfigure(2, weight=0)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("bees.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12, width=35)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        self.add_btn = ttk.Button(btn_frame, text=bc.get_lang_text("bees.add"),
                                  command=self._add_new)
        self.add_btn.pack(side='left', padx=5)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                                     command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        # 右侧区域
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)   # 文本域可伸缩

        # 字段：min_ticks_in_hive
        row = 0
        frame_min = tk.Frame(right_frame)
        frame_min.grid(row=row, column=0, sticky='ew', padx=5, pady=2)
        frame_min.columnconfigure(1, weight=1)
        tk.Label(frame_min, text=bc.get_lang_text("bees.min_ticks")).grid(row=0, column=0, sticky='w')
        self.min_ticks_var = tk.StringVar(value="0")
        self.min_ticks_entry = tk.Entry(frame_min, textvariable=self.min_ticks_var, width=10)
        self.min_ticks_entry.grid(row=0, column=1, sticky='w', padx=5)
        row += 1

        # 字段：ticks_in_hive
        frame_ticks = tk.Frame(right_frame)
        frame_ticks.grid(row=row, column=0, sticky='ew', padx=5, pady=2)
        frame_ticks.columnconfigure(1, weight=1)
        tk.Label(frame_ticks, text=bc.get_lang_text("bees.ticks")).grid(row=0, column=0, sticky='w')
        self.ticks_var = tk.StringVar(value="0")
        self.ticks_entry = tk.Entry(frame_ticks, textvariable=self.ticks_var, width=10)
        self.ticks_entry.grid(row=0, column=1, sticky='w', padx=5)
        row += 1

        # 标签：entity_data
        tk.Label(right_frame, text=bc.get_lang_text("bees.entity_data_label")).grid(row=row, column=0, sticky='w', padx=5, pady=(10,0))
        row += 1

        # 多行文本域
        self.text_area = ScrolledText(right_frame, height=8, width=70, wrap='word', font=('Consolas', 10))
        self.text_area.grid(row=row, column=0, sticky='nsew', padx=5, pady=5)
        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("bees.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, pady=10)

        # 默认添加一个空白条目
        self._add_new()

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_form()

    def _clear_form(self):
        self.min_ticks_var.set("0")
        self.ticks_var.set("0")
        self.text_area.delete('1.0', tk.END)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        try:
            del self.bees[self.current_index]
            self._refresh_listbox()
            self.current_index = None
            self._clear_form()
            if self.bees:
                self.listbox.selection_set(0)
                self._on_select()
            messagebox.showinfo(bc.get_lang_text("deleted.title"),
                                bc.get_lang_text("msg.deleted.modifier"))
        except Exception as e:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("msg.error.failed_delete").format(error=str(e)))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, bee in enumerate(self.bees):
            preview = f"B{idx+1}: min={bee['min_ticks']} ticks={bee['ticks']}"
            self.listbox.insert(tk.END, preview)

    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.current_index = None
            return
        idx = selection[0]
        self.current_index = idx
        bee = self.bees[idx]
        self.min_ticks_var.set(str(bee['min_ticks']))
        self.ticks_var.set(str(bee['ticks']))
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', bee['entity_data'])

    def _save_current(self):
        try:
            # 获取并验证 min_ticks
            min_ticks_str = self.min_ticks_var.get().strip()
            if not min_ticks_str:
                min_ticks = 0
            else:
                min_ticks = int(min_ticks_str)
                if min_ticks < 0:
                    raise ValueError

            ticks_str = self.ticks_var.get().strip()
            if not ticks_str:
                ticks = 0
            else:
                ticks = int(ticks_str)
                if ticks < 0:
                    raise ValueError

            entity_data = self.text_area.get('1.0', 'end-1c').strip()
            if not entity_data:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("bees.error.empty_entity_data"))
                return

            bee_entry = {
                "min_ticks": min_ticks,
                "ticks": ticks,
                "entity_data": entity_data
            }

            if self.current_index is None:
                self.bees.append(bee_entry)
                self._refresh_listbox()
                new_idx = len(self.bees) - 1
                self.listbox.selection_set(new_idx)
                self.current_index = new_idx
            else:
                self.bees[self.current_index] = bee_entry
                self._refresh_listbox()
                self.listbox.selection_set(self.current_index)

            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("bees.error.invalid_ticks"))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(bc.get_lang_text("critical.error.title"),
                                 bc.get_lang_text("msg.error.unexpected").format(error=str(e)))

    def get_nbt(self):
        if not self.bees:
            return ""
        items = []
        for bee in self.bees:
            # 注意 entity_data 内容应该已经是合法的 NBT 对象，无需额外大括号
            # 确保 entity_data 字符串开头可能是 { 或类似，但为了安全我们直接拼接
            item = f'{{min_ticks_in_hive:{bee["min_ticks"]},ticks_in_hive:{bee["ticks"]},entity_data:{bee["entity_data"]}}}'
            items.append(item)
        return f'bees=[{",".join(items)}]'