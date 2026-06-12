import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import traceback
import affiliated.kernel.basic_components as bc

class BundleContentsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.items = []          # each: {"id":str, "count":int, "components":str}
        self.current_index = None

        # 使用 PanedWindow 或简单 grid，设置权重
        self.grid_columnconfigure(0, weight=0)  # 左侧列表不伸缩
        self.grid_columnconfigure(1, weight=1)  # 右侧伸缩
        self.grid_rowconfigure(0, weight=1)

        # 左侧列表框架
        left_frame = tk.Frame(self, width=200)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)  # 固定宽度
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("bundle_contents.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        self.add_btn = ttk.Button(btn_frame, text=bc.get_lang_text("bundle_contents.add"),
                                  command=self._add_new)
        self.add_btn.pack(side='left', padx=5)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                                     command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        # 右侧编辑框架
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_rowconfigure(3, weight=1)   # 让 components 文本框可伸展

        row = 0
        # ID
        tk.Label(right_frame, text=bc.get_lang_text("bundle_contents.id")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.id_entry = tk.Entry(right_frame, width=30)
        self.id_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # Count
        tk.Label(right_frame, text=bc.get_lang_text("bundle_contents.count")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.count_entry = tk.Entry(right_frame, width=10)
        self.count_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # Components
        tk.Label(right_frame, text=bc.get_lang_text("bundle_contents.components")).grid(row=row, column=0, sticky='nw', padx=5, pady=2)
        self.components_text = ScrolledText(right_frame, height=8, wrap='word', font=('Consolas', 10))
        self.components_text.grid(row=row, column=1, sticky='nsew', padx=5, pady=2)
        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("bundle_contents.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 初始添加一个空条目（或者不加，但为了方便，添加一个空）
        self._add_new()

    # ---------- 方法实现 ----------
    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_form()

    def _clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.count_entry.delete(0, tk.END)
        self.components_text.delete('1.0', tk.END)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        try:
            del self.items[self.current_index]
            self._refresh_listbox()
            self.current_index = None
            self._clear_form()
            if self.items:
                self.listbox.selection_set(0)
                self._on_select()
            messagebox.showinfo(bc.get_lang_text("deleted.title"),
                                bc.get_lang_text("msg.deleted.modifier"))
        except Exception as e:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("msg.error.failed_delete").format(error=str(e)))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, it in enumerate(self.items):
            self.listbox.insert(tk.END, f"{idx+1}: {it['id']} x{it['count']}")

    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.current_index = None
            return
        idx = selection[0]
        self.current_index = idx
        it = self.items[idx]
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, it['id'])
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, str(it['count']))
        self.components_text.delete('1.0', tk.END)
        self.components_text.insert('1.0', it['components'])

    def _save_current(self):
        try:
            id_val = self.id_entry.get().strip()
            if not id_val:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("bundle_contents.error.id_empty"))
                return
            count_str = self.count_entry.get().strip()
            count = int(count_str) if count_str else 1
            if not (0 <= count <= 99):
                raise ValueError
            comp = self.components_text.get('1.0', 'end-1c').strip()
            # comp 可以为空字符串
            entry = {"id": id_val, "count": count, "components": comp}
            if self.current_index is None:
                self.items.append(entry)
                self._refresh_listbox()
                new_idx = len(self.items) - 1
                self.listbox.selection_set(new_idx)
                self.current_index = new_idx
            else:
                self.items[self.current_index] = entry
                self._refresh_listbox()
                self.listbox.selection_set(self.current_index)
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("bundle_contents.error.invalid_count"))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(bc.get_lang_text("critical.error.title"),
                                 bc.get_lang_text("msg.error.unexpected").format(error=str(e)))

    def get_nbt(self):
        if not self.items:
            return ""
        parts = []
        for it in self.items:
            if it['components']:
                parts.append(f'{{id:"{it["id"]}",count:{it["count"]},components:{{{it["components"]}}}}}')
            else:
                parts.append(f'{{id:"{it["id"]}",count:{it["count"]}}}')
        return f'bundle_contents=[{",".join(parts)}]'