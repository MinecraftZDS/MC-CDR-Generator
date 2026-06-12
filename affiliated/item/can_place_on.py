import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class CanPlaceOnWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)
        self.blocks = []  # list of block id strings
        self.current_index = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left.grid_rowconfigure(0, weight=0)
        left.grid_rowconfigure(1, weight=1)
        left.grid_rowconfigure(2, weight=0)
        left.grid_columnconfigure(0, weight=1)

        tk.Label(left, text=bc.get_lang_text("can_place_on.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left)
        btn_frame.grid(row=2, column=0, pady=10)
        self.add_btn = ttk.Button(btn_frame, text=bc.get_lang_text("can_place_on.add"), command=self._add_new)
        self.add_btn.pack(side='left', padx=5)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"), command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        right = tk.Frame(self, relief='sunken', bd=1)
        right.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right.grid_columnconfigure(1, weight=1)

        tk.Label(right, text=bc.get_lang_text("can_place_on.block_id")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.id_entry = tk.Entry(right, width=40)
        self.id_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.save_btn = ttk.Button(right, text=bc.get_lang_text("can_place_on.save"), command=self._save_current)
        self.save_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self._add_new()

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self.id_entry.delete(0, tk.END)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"), bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"), bc.get_lang_text("msg.confirm.delete")):
            return
        del self.blocks[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self.id_entry.delete(0, tk.END)
        if self.blocks:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"), bc.get_lang_text("msg.deleted.modifier"))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, blk in enumerate(self.blocks):
            self.listbox.insert(tk.END, f"{idx+1}: {blk}")

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, self.blocks[idx])

    def _save_current(self):
        block_id = self.id_entry.get().strip()
        if not block_id:
            messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("can_place_on.error.empty"))
            return
        if self.current_index is None:
            self.blocks.append(block_id)
            self._refresh_listbox()
            self.listbox.selection_set(len(self.blocks)-1)
            self.current_index = len(self.blocks)-1
        else:
            self.blocks[self.current_index] = block_id
            self._refresh_listbox()
            self.listbox.selection_set(self.current_index)
        messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.blocks:
            return ""
        blocks_json = ','.join(f'"{b}"' for b in self.blocks)
        return f'can_place_on={{blocks:[{blocks_json}]}}'