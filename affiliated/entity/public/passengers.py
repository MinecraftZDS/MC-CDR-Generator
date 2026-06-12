import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import affiliated.kernel.basic_components as bc

class PassengersWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.passengers = []   # 存储每个乘客的 NBT 字符串（完整对象）
        self.current_index = None

        # 布局：左侧列表，右侧编辑区
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("passengers.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("passengers.add"), command=self._add).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"), command=self._remove).pack(side='left', padx=5)

        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        self.text = ScrolledText(right_frame, height=10, wrap='word', font=('Consolas',10))
        self.text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("passengers.save"), command=self._save_current)
        self.save_btn.grid(row=1, column=0, pady=10)

        self._refresh_listbox()
        self._add()  # 添加一个空条目

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, p in enumerate(self.passengers):
            preview = p[:30] + "..." if len(p) > 30 else p
            self.listbox.insert(tk.END, f"{idx+1}: {preview}")

    def _add(self):
        self.passengers.append("{}")
        self._refresh_listbox()
        self.listbox.selection_set(len(self.passengers)-1)
        self.current_index = len(self.passengers)-1
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', "{}")

    def _remove(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"), bc.get_lang_text("msg.warning.no_modifier"))
            return
        if len(self.passengers) == 1:
            messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("passengers.error.cannot_remove_last"))
            return
        del self.passengers[self.current_index]
        self._refresh_listbox()
        if self.passengers:
            self.listbox.selection_set(0)
            self._on_select()
        else:
            self.current_index = None
            self.text.delete('1.0', tk.END)
        messagebox.showinfo(bc.get_lang_text("deleted.title"), bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', self.passengers[idx])

    def _save_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"), bc.get_lang_text("msg.warning.no_modifier"))
            return
        content = self.text.get('1.0', 'end-1c').strip()
        if not content:
            content = "{}"
        self.passengers[self.current_index] = content
        self._refresh_listbox()
        messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.passengers:
            return ""
        items = ','.join(self.passengers)
        return f'Passengers:[{items}]'