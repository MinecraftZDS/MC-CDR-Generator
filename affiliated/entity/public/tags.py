import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class TagsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.tags = []   # 存储字符串
        self.current_index = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("tags.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("tags.add"), command=self._add).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"), command=self._remove).pack(side='left', padx=5)

        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        tk.Label(right_frame, text=bc.get_lang_text("tags.value")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.entry = tk.Entry(right_frame, width=40)
        self.entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("tags.save"), command=self._save_current)
        self.save_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self._refresh_listbox()
        self._add()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, tag in enumerate(self.tags):
            self.listbox.insert(tk.END, f"{idx+1}: {tag}")

    def _add(self):
        self.tags.append("")
        self._refresh_listbox()
        self.listbox.selection_set(len(self.tags)-1)
        self.current_index = len(self.tags)-1
        self.entry.delete(0, tk.END)

    def _remove(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"), bc.get_lang_text("msg.warning.no_modifier"))
            return
        if len(self.tags) == 1:
            messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("tags.error.cannot_remove_last"))
            return
        del self.tags[self.current_index]
        self._refresh_listbox()
        if self.tags:
            self.listbox.selection_set(0)
            self._on_select()
        else:
            self.current_index = None
            self.entry.delete(0, tk.END)
        messagebox.showinfo(bc.get_lang_text("deleted.title"), bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.tags[idx])

    def _save_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"), bc.get_lang_text("msg.warning.no_modifier"))
            return
        val = self.entry.get().strip()
        if not val:
            val = ""
        self.tags[self.current_index] = val
        self._refresh_listbox()
        messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.tags:
            return ""
        items = ','.join(f'"{tag}"' for tag in self.tags)
        return f'Tags:[{items}]'