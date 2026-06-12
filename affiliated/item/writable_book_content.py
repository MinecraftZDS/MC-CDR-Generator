import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import affiliated.kernel.basic_components as bc

class WritableBookContentWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.pages = []          # 存储每个页面的文本内容（字符串列表）
        self.current_index = None

        # 布局
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 左侧列表区域
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("writable_book_content.pages_list")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("writable_book_content.add_page"),
                   command=self._add_page).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_page).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        self.text_area = ScrolledText(right_frame, height=15, wrap='word', font=('Consolas', 10))
        self.text_area.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # 按钮行：保存当前页面 + 保存全书
        btn_row = tk.Frame(right_frame)
        btn_row.grid(row=1, column=0, pady=5)
        self.save_page_btn = ttk.Button(btn_row, text=bc.get_lang_text("writable_book_content.save_page"),
                                        command=self._save_current_page)
        self.save_page_btn.pack(side='left', padx=5)
        self.save_book_btn = ttk.Button(btn_row, text=bc.get_lang_text("writable_book_content.save_book"),
                                        command=self._save_book)
        self.save_book_btn.pack(side='left', padx=5)

        # 初始添加一页空白
        self._add_page()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, page_content in enumerate(self.pages):
            preview = page_content[:30] + "..." if len(page_content) > 30 else page_content
            self.listbox.insert(tk.END, f"Page {idx+1}: {preview}")

    def _add_page(self):
        # 如果已有100页，禁止添加
        if len(self.pages) >= 100:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("writable_book_content.error.max_pages"))
            return
        self.pages.append("")
        self._refresh_listbox()
        # 自动选中新添加的页
        new_idx = len(self.pages) - 1
        self.listbox.selection_set(new_idx)
        self.current_index = new_idx
        self.text_area.delete('1.0', tk.END)

    def _remove_page(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if len(self.pages) == 1:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("writable_book_content.error.cannot_remove_last"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.pages[self.current_index]
        self._refresh_listbox()
        # 如果删除后还有页面，选中第一页
        if self.pages:
            self.listbox.selection_set(0)
            self._on_select()
        else:
            # 理论上不会为空，但安全处理
            self.current_index = None
            self.text_area.delete('1.0', tk.END)
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        # 清空并加载当前页面内容
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', self.pages[idx])

    def _save_current_page(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        content = self.text_area.get('1.0', 'end-1c')
        self.pages[self.current_index] = content
        self._refresh_listbox()
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def _save_book(self):
        # 确保至少有一页（实际上初始化时就有一页，但可能空）
        if not self.pages:
            self.pages = [""]
        # 验证页数不超过100（已限制添加，但防止手动修改）
        if len(self.pages) > 100:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("writable_book_content.error.max_pages_save"))
            return
        # 保存当前未保存的页面内容
        if self.current_index is not None:
            self.pages[self.current_index] = self.text_area.get('1.0', 'end-1c')
            self._refresh_listbox()
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.pages:
            return ""
        # 生成 pages 字符串数组
        pages_json = json.dumps(self.pages, separators=(',', ':'))
        return f'writable_book_content={{pages:{pages_json}}}'