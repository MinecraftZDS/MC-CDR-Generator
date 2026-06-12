import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import affiliated.kernel.basic_components as bc

class AttributeModifierWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.modifiers = []
        self.current_index = None

        # 主网格
        self.grid_columnconfigure(0, weight=1)  # 左侧
        self.grid_columnconfigure(1, weight=2)  # 右侧
        self.grid_rowconfigure(0, weight=1)

        # ---------- 左侧区域 ----------
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_rowconfigure(0, weight=0)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_rowconfigure(2, weight=0)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("label.attribute_modifier")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12, width=35)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                                     command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        # ---------- 右侧区域 ----------
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=0)
        right_frame.grid_columnconfigure(1, weight=1)
        row = 0

        tk.Label(right_frame, text=bc.get_lang_text("attribute.amount")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.amount_entry = tk.Entry(right_frame, width=25)
        self.amount_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        tk.Label(right_frame, text=bc.get_lang_text("attribute.id")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.id_entry = tk.Entry(right_frame, width=25)
        self.id_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        tk.Label(right_frame, text=bc.get_lang_text("attribute.operation")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.operation_combo = ttk.Combobox(right_frame, values=[
            "add_value",
            "add_multiplied_base",
            "add_multiplied_total"
        ], state='readonly', width=22)
        self.operation_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        if self.operation_combo['values']:
            self.operation_combo.current(0)
        row += 1

        tk.Label(right_frame, text=bc.get_lang_text("attribute.slot")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.slot_combo = ttk.Combobox(right_frame, values=[
            "head", "chest", "legs", "feet",
            "any", "mainhand", "offhand", "body", "saddle"
        ], state='readonly', width=22)
        self.slot_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        if self.slot_combo['values']:
            self.slot_combo.current(0)
        row += 1

        tk.Label(right_frame, text=bc.get_lang_text("attribute.type")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.type_entry = tk.Entry(right_frame, width=25)
        self.type_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("button.save.attributemodifier"),
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_form()

    def _clear_form(self):
        self.amount_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        if self.operation_combo['values']:
            self.operation_combo.current(0)
        if self.slot_combo['values']:
            self.slot_combo.current(0)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        try:
            del self.modifiers[self.current_index]
            self._refresh_listbox()
            self.current_index = None
            self._clear_form()
            if self.modifiers:
                self.listbox.selection_set(0)
                self._on_select()
            messagebox.showinfo(bc.get_lang_text("deleted.title"),
                                bc.get_lang_text("msg.deleted.modifier"))
        except Exception as e:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("msg.error.failed_delete").format(error=str(e)))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for mod in self.modifiers:
            # 显示格式：类型 (运算方式) — 这部分可以保留原样，因为 type 和 operation 是用户输入或固定的英文
            self.listbox.insert(tk.END, f"{mod['type']} ({mod['operation']})")

    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.current_index = None
            return
        idx = selection[0]
        self.current_index = idx
        mod = self.modifiers[idx]
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(mod['amount']))
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, mod['id'])
        self.operation_combo.set(mod['operation'])
        self.slot_combo.set(mod['slot'])
        self.type_entry.delete(0, tk.END)
        self.type_entry.insert(0, mod['type'])

    def _save_current(self):
        try:
            amount_str = self.amount_entry.get().strip()
            if not amount_str:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.amount_empty"))
                return
            try:
                amount = float(amount_str)
            except ValueError:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.amount_invalid"))
                return

            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.id_empty"))
                return

            operation = self.operation_combo.get()
            if not operation:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.operation_empty"))
                return

            slot = self.slot_combo.get()
            if not slot:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.slot_empty"))
                return

            type_str = self.type_entry.get().strip()
            if not type_str:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msg.error.type_empty"))
                return

            modifier = {
                "amount": amount,
                "id": id_str,
                "operation": operation,
                "slot": slot,
                "type": type_str
            }

            if self.current_index is None:
                self.modifiers.append(modifier)
                self._refresh_listbox()
                new_idx = len(self.modifiers) - 1
                self.listbox.selection_set(new_idx)
                self.current_index = new_idx
            else:
                self.modifiers[self.current_index] = modifier
                self._refresh_listbox()
                self.listbox.selection_set(self.current_index)

            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(bc.get_lang_text("critical.error.title"),
                                 bc.get_lang_text("msg.error.unexpected").format(error=str(e)))

    def get_nbt(self):
        if not self.modifiers:
            return ""
        items = []
        for mod in self.modifiers:
            id_escaped = mod['id'].replace('"', '\\"')
            type_escaped = mod['type'].replace('"', '\\"')
            item = f'{{amount:{mod["amount"]},id:"{id_escaped}",operation:"{mod["operation"]}",slot:"{mod["slot"]}",type:"{type_escaped}"}}'
            items.append(item)
        return f'attribute_modifiers=[{",".join(items)}]'