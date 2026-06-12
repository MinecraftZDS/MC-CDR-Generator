import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class RepairableWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.items = []   # 存储物品 ID
        self.current_index = None

        # 布局
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 左侧列表
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("repairable.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("repairable.add"),
                   command=self._add_item).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_item).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        tk.Label(right_frame, text=bc.get_lang_text("repairable.id_label")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.id_entry = tk.Entry(right_frame, width=40)
        self.id_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("repairable.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self._add_new()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, rid in enumerate(self.items):
            self.listbox.insert(tk.END, f"{idx+1}: {rid}")

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self.id_entry.delete(0, tk.END)

    def _add_item(self):
        self.current_index = None
        self.id_entry.delete(0, tk.END)

    def _remove_item(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.items[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self.id_entry.delete(0, tk.END)
        if self.items:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, self.items[idx])

    def _save_current(self):
        val = self.id_entry.get().strip()
        if not val:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("repairable.error.empty"))
            return
        if self.current_index is None:
            self.items.append(val)
            self._refresh_listbox()
            new_idx = len(self.items) - 1
            self.listbox.selection_set(new_idx)
            self.current_index = new_idx
        else:
            self.items[self.current_index] = val
            self._refresh_listbox()
            self.listbox.selection_set(self.current_index)
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.items:
            return ""
        items_json = ','.join(f'"{item}"' for item in self.items)
        return f'repairable={{items:[{items_json}]}}'