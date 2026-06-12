import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os
import traceback
import affiliated.kernel.basic_components as bc

class SuspiciousStewEffectsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.effects = []   # 每个元素 {"duration": int, "id": str}
        self.current_index = None

        # 加载效果ID列表
        self.potion_effects = self._load_potion_effects()

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

        tk.Label(left_frame, text=bc.get_lang_text("suspicious_stew_effects.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("suspicious_stew_effects.add"),
                   command=self._add_effect).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_effect).pack(side='left', padx=5)

        # 右侧编辑区
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        # 效果 ID 下拉
        tk.Label(right_frame, text=bc.get_lang_text("suspicious_stew_effects.id")).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.id_combo = ttk.Combobox(right_frame, values=self.potion_effects, state='readonly', width=30)
        self.id_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # 持续时间
        tk.Label(right_frame, text=bc.get_lang_text("suspicious_stew_effects.duration")).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.duration_entry = tk.Entry(right_frame, width=10)
        self.duration_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        # 保存按钮
        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("suspicious_stew_effects.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self._add_new()

    def _load_potion_effects(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('potion_effects', [])
        except:
            return []

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, eff in enumerate(self.effects):
            eff_id = eff.get('id', '?')
            dur = eff.get('duration', 160)
            self.listbox.insert(tk.END, f"{idx+1}: {eff_id} dur:{dur}")

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self.id_combo.set('')
        self.duration_entry.delete(0, tk.END)

    def _add_effect(self):
        self.current_index = None
        self.id_combo.set('')
        self.duration_entry.delete(0, tk.END)

    def _remove_effect(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.effects[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self.id_combo.set('')
        self.duration_entry.delete(0, tk.END)
        if self.effects:
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
        eff = self.effects[idx]
        self.id_combo.set(eff.get('id', ''))
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, str(eff.get('duration', 160)))

    def _save_current(self):
        effect_id = self.id_combo.get().strip()
        if not effect_id:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("suspicious_stew_effects.error.no_id"))
            return
        dur_str = self.duration_entry.get().strip()
        duration = 160
        if dur_str:
            try:
                duration = int(dur_str)
                if duration < 0:
                    raise ValueError
            except:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("suspicious_stew_effects.error.invalid_duration"))
                return
        new_effect = {"id": effect_id, "duration": duration}
        if self.current_index is None:
            self.effects.append(new_effect)
            self._refresh_listbox()
            new_idx = len(self.effects) - 1
            self.listbox.selection_set(new_idx)
            self.current_index = new_idx
        else:
            self.effects[self.current_index] = new_effect
            self._refresh_listbox()
            self.listbox.selection_set(self.current_index)
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.effects:
            return ""
        parts = []
        for eff in self.effects:
            parts.append(f'{{duration:{eff["duration"]},id:"{eff["id"]}"}}')
        return f'suspicious_stew_effects=[{",".join(parts)}]'