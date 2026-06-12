import tkinter as tk
from tkinter import ttk, messagebox
import json
import affiliated.kernel.basic_components as bc
from affiliated.kernel.text_components import TextComponentsManager

class WrittenBookContentWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.author = ""
        self.generation = 0
        self.title = ""
        self.pages = []          # 存储每个页面的文本组件列表
        self.current_page_index = None

        # 使用网格布局，各行权重
        self.grid_rowconfigure(0, weight=0)  # 基础属性
        self.grid_rowconfigure(1, weight=1)  # 页面列表
        self.grid_rowconfigure(2, weight=0)  # 按钮行
        self.grid_columnconfigure(0, weight=1)

        # ---------- 基础属性区域 ----------
        frame_top = ttk.LabelFrame(self, text=bc.get_lang_text("written_book_content.basic_info"))
        frame_top.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        frame_top.columnconfigure(1, weight=1)

        # 作者
        tk.Label(frame_top, text=bc.get_lang_text("written_book_content.author")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.author_entry = tk.Entry(frame_top)
        self.author_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # 世代
        tk.Label(frame_top, text=bc.get_lang_text("written_book_content.generation")).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.generation_combo = ttk.Combobox(frame_top, values=[0,1,2,3], state='readonly', width=5)
        self.generation_combo.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.generation_combo.current(0)

        # 标题
        tk.Label(frame_top, text=bc.get_lang_text("written_book_content.title")).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.title_entry = tk.Entry(frame_top)
        self.title_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        # ---------- 页面列表区域 ----------
        frame_mid = ttk.LabelFrame(self, text=bc.get_lang_text("written_book_content.pages_list"))
        frame_mid.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        frame_mid.grid_rowconfigure(0, weight=1)
        frame_mid.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(frame_mid)
        self.listbox.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_page_select)

        # 页面列表按钮
        btn_page = tk.Frame(frame_mid)
        btn_page.grid(row=1, column=0, pady=5)
        ttk.Button(btn_page, text=bc.get_lang_text("written_book_content.add_page"),
                   command=self._add_page).pack(side='left', padx=5)
        ttk.Button(btn_page, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_page).pack(side='left', padx=5)

        # ---------- 底部两个按钮 ----------
        frame_bottom = tk.Frame(self)
        frame_bottom.grid(row=2, column=0, pady=10)
        ttk.Button(frame_bottom, text=bc.get_lang_text("written_book_content.edit_content"),
                   command=self._open_editor).pack(side='left', padx=10)
        ttk.Button(frame_bottom, text=bc.get_lang_text("written_book_content.save_book"),
                   command=self._save_book).pack(side='left', padx=10)

        # 初始化一个空白页面
        self._add_page()

    # ---------- 页面列表管理 ----------
    def _refresh_page_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, page_comps in enumerate(self.pages):
            comp_count = len(page_comps)
            self.listbox.insert(tk.END, f"Page {idx+1} ({comp_count} components)")

    def _add_page(self):
        self.pages.append([])
        self._refresh_page_listbox()
        new_idx = len(self.pages) - 1
        self.listbox.selection_set(new_idx)
        self.current_page_index = new_idx

    def _remove_page(self):
        if self.current_page_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if len(self.pages) == 1:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("written_book_content.error.cannot_remove_last"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.pages[self.current_page_index]
        self._refresh_page_listbox()
        if self.pages:
            self.listbox.selection_set(0)
            self._on_page_select()
        else:
            self.current_page_index = None
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_page_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_page_index = None
        else:
            self.current_page_index = sel[0]

    # ---------- 子窗口编辑页面内容 ----------
    def _open_editor(self):
        if self.current_page_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return

        win = tk.Toplevel(self)
        win.title(bc.get_lang_text("written_book_content.editor_title"))
        win.geometry("700x550")
        win.transient(self)
        win.grab_set()

        # 可滚动区域
        canvas = tk.Canvas(win, highlightthickness=0)
        v_scroll = tk.Scrollbar(win, orient='vertical', command=canvas.yview)
        h_scroll = tk.Scrollbar(win, orient='horizontal', command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))

        # 文本组件管理器
        page_mgr = TextComponentsManager(inner)
        page_mgr.pack(fill='both', expand=True)
        current_page_comps = self.pages[self.current_page_index]
        page_mgr.components = current_page_comps.copy()
        page_mgr._refresh_listbox()
        page_mgr._clear_form()

        # 按钮
        btn_frame = tk.Frame(inner)
        btn_frame.pack(pady=10)
        def save_and_close():
            self.pages[self.current_page_index] = page_mgr.get_components()
            self._refresh_page_listbox()
            win.destroy()
        ttk.Button(btn_frame, text=bc.get_lang_text("written_book_content.save_page"),
                   command=save_and_close).pack(side='left', padx=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("written_book_content.cancel"),
                   command=win.destroy).pack(side='left', padx=10)

    # ---------- 保存全书 ----------
    def _save_book(self):
        # 保存前确保当前页面已保存（避免丢失未保存的修改）
        # 但编辑器在子窗口中保存时才更新，主窗口没有临时编辑区，所以无需额外操作
        author = self.author_entry.get().strip()
        if not author:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("written_book_content.error.author_empty"))
            return
        try:
            generation = int(self.generation_combo.get().strip())
            if generation not in [0,1,2,3]:
                raise ValueError
        except:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("written_book_content.error.generation_invalid"))
            return
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("written_book_content.error.title_empty"))
            return
        self.author = author
        self.generation = generation
        self.title = title
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    # ---------- NBT 生成 ----------
    def get_nbt(self):
        if not self.author or not self.title:
            return ""
        pages_json = []
        for page_comps in self.pages:
            filtered = [{k:v for k,v in comp.items() if k != 'type'} for comp in page_comps]
            pages_json.append(filtered)
        obj = {
            "author": self.author,
            "generation": self.generation,
            "title": self.title,
            "pages": pages_json
        }
        return f'written_book_content={json.dumps(obj, separators=(",", ":"))}'