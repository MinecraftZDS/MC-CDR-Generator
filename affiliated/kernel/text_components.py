import tkinter as tk
from tkinter import ttk, messagebox
import json
import traceback
import affiliated.kernel.basic_components as bc

class TextComponentsManager(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.components = []
        self.current_index = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("text_components.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        self.add_btn = ttk.Button(btn_frame, text=bc.get_lang_text("text_components.add"),
                                  command=self._add_new)
        self.add_btn.pack(side='left', padx=5)
        self.remove_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                                     command=self._remove_current)
        self.remove_btn.pack(side='left', padx=5)

        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)

        row = 0
        type_frame = tk.Frame(right_frame)
        type_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
        self.type_var = tk.StringVar(value="text")
        types = ["text", "translate", "keybind", "score", "selector"]
        for t in types:
            rb = tk.Radiobutton(type_frame, text=t, variable=self.type_var, value=t)
            rb.pack(side='left', padx=5)
        row += 1

        self.content_frame = tk.Frame(right_frame)
        self.content_frame.grid(row=row, column=0, columnspan=2, sticky='nsew', pady=5)
        row += 1

        style_frame = tk.LabelFrame(right_frame, text=bc.get_lang_text("text_components.style"))
        style_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
        tk.Label(style_frame, text=bc.get_lang_text("text_components.color")).grid(row=0, column=0, sticky='w', padx=5)
        self.color_entry = tk.Entry(style_frame, width=12)
        self.color_entry.grid(row=0, column=1, sticky='w', padx=5)
        self.bold_var = tk.BooleanVar()
        self.italic_var = tk.BooleanVar()
        self.underlined_var = tk.BooleanVar()
        self.strikethrough_var = tk.BooleanVar()
        self.obfuscated_var = tk.BooleanVar()
        chk_frame = tk.Frame(style_frame)
        chk_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=5)
        tk.Checkbutton(chk_frame, text="bold", variable=self.bold_var).pack(side='left', padx=2)
        tk.Checkbutton(chk_frame, text="italic", variable=self.italic_var).pack(side='left', padx=2)
        tk.Checkbutton(chk_frame, text="underlined", variable=self.underlined_var).pack(side='left', padx=2)
        tk.Checkbutton(chk_frame, text="strikethrough", variable=self.strikethrough_var).pack(side='left', padx=2)
        tk.Checkbutton(chk_frame, text="obfuscated", variable=self.obfuscated_var).pack(side='left', padx=2)
        row += 1

        self.save_btn = ttk.Button(right_frame, text=bc.get_lang_text("text_components.save"),
                                   command=self._save_current)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        self.type_var.trace('w', lambda *a: self._refresh_dynamic_ui())
        self._refresh_dynamic_ui()
        self._add_new()

    def _refresh_dynamic_ui(self):
        for w in self.content_frame.winfo_children():
            w.destroy()
        etype = self.type_var.get()
        if etype in ["text", "translate", "keybind"]:
            label_text = bc.get_lang_text(f"text_components.{etype}_label")
            tk.Label(self.content_frame, text=label_text).pack(anchor='w')
            self.content_entry = tk.Entry(self.content_frame, width=50)
            self.content_entry.pack(fill='x', padx=5, pady=2)
        elif etype == "score":
            tk.Label(self.content_frame, text=bc.get_lang_text("text_components.score_name")).pack(anchor='w')
            self.score_name_entry = tk.Entry(self.content_frame, width=30)
            self.score_name_entry.pack(fill='x', padx=5, pady=2)
            tk.Label(self.content_frame, text=bc.get_lang_text("text_components.score_objective")).pack(anchor='w')
            self.score_objective_entry = tk.Entry(self.content_frame, width=30)
            self.score_objective_entry.pack(fill='x', padx=5, pady=2)
        elif etype == "selector":
            tk.Label(self.content_frame, text=bc.get_lang_text("text_components.selector_selector")).pack(anchor='w')
            self.selector_entry = tk.Entry(self.content_frame, width=30)
            self.selector_entry.pack(fill='x', padx=5, pady=2)
            tk.Label(self.content_frame, text=bc.get_lang_text("text_components.selector_separator")).pack(anchor='w')
            self.separator_entry = tk.Entry(self.content_frame, width=30)
            self.separator_entry.pack(fill='x', padx=5, pady=2)

    def _add_new(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self._clear_form()

    def _clear_form(self):
        self.type_var.set("text")
        if hasattr(self, 'content_entry'):
            self.content_entry.delete(0, tk.END)
        if hasattr(self, 'score_name_entry'):
            self.score_name_entry.delete(0, tk.END)
            self.score_objective_entry.delete(0, tk.END)
        if hasattr(self, 'selector_entry'):
            self.selector_entry.delete(0, tk.END)
            self.separator_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.bold_var.set(False)
        self.italic_var.set(False)
        self.underlined_var.set(False)
        self.strikethrough_var.set(False)
        self.obfuscated_var.set(False)

    def _remove_current(self):
        if self.current_index is None:
            messagebox.showwarning(bc.get_lang_text("warning.title"),
                                   bc.get_lang_text("msg.warning.no_modifier"))
            return
        if not messagebox.askyesno(bc.get_lang_text("confirm.delete.title"),
                                   bc.get_lang_text("msg.confirm.delete")):
            return
        del self.components[self.current_index]
        self._refresh_listbox()
        self.current_index = None
        self._clear_form()
        if self.components:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, comp in enumerate(self.components):
            # 简单显示类型和摘要
            typ = comp.get('type', 'unknown')
            if typ in ['text', 'translate', 'keybind']:
                txt = comp.get(typ, '')
                display = f"{typ}: {txt[:30]}"
            elif typ == 'score':
                obj = comp.get('score', {}).get('objective', '?')
                name = comp.get('score', {}).get('name', '?')
                display = f"score: {name}@{obj}"
            elif typ == 'selector':
                sel = comp.get('selector', '')
                display = f"selector: {sel}"
            else:
                display = typ
            self.listbox.insert(tk.END, display)

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            return
        idx = sel[0]
        self.current_index = idx
        comp = self.components[idx]
        self.type_var.set(comp.get('type', 'text'))
        etype = comp['type']
        if etype in ['text', 'translate', 'keybind']:
            self.content_entry.delete(0, tk.END)
            self.content_entry.insert(0, comp.get(etype, ''))
        elif etype == 'score':
            self.score_name_entry.delete(0, tk.END)
            self.score_name_entry.insert(0, comp['score'].get('name', ''))
            self.score_objective_entry.delete(0, tk.END)
            self.score_objective_entry.insert(0, comp['score'].get('objective', ''))
        elif etype == 'selector':
            self.selector_entry.delete(0, tk.END)
            self.selector_entry.insert(0, comp.get('selector', ''))
            self.separator_entry.delete(0, tk.END)
            self.separator_entry.insert(0, comp.get('separator', ''))
        # 样式
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, comp.get('color', ''))
        self.bold_var.set(comp.get('bold', False))
        self.italic_var.set(comp.get('italic', False))
        self.underlined_var.set(comp.get('underlined', False))
        self.strikethrough_var.set(comp.get('strikethrough', False))
        self.obfuscated_var.set(comp.get('obfuscated', False))

    def _save_current(self):
        try:
            etype = self.type_var.get()
            new_comp = {"type": etype}
            if etype in ['text', 'translate', 'keybind']:
                val = self.content_entry.get().strip()
                if not val:
                    messagebox.showerror(bc.get_lang_text("error.title"), f"{etype} content cannot be empty.")
                    return
                new_comp[etype] = val
            elif etype == 'score':
                name = self.score_name_entry.get().strip()
                obj = self.score_objective_entry.get().strip()
                if not name or not obj:
                    messagebox.showerror(bc.get_lang_text("error.title"), "Score name and objective required.")
                    return
                new_comp['score'] = {"name": name, "objective": obj}
            elif etype == 'selector':
                sel = self.selector_entry.get().strip()
                if not sel:
                    messagebox.showerror(bc.get_lang_text("error.title"), "Selector cannot be empty.")
                    return
                new_comp['selector'] = sel
                sep = self.separator_entry.get().strip()
                if sep:
                    new_comp['separator'] = sep
            color = self.color_entry.get().strip()
            if color:
                new_comp['color'] = color
            if self.bold_var.get():
                new_comp['bold'] = True
            new_comp['italic'] = self.italic_var.get()
            if self.underlined_var.get():
                new_comp['underlined'] = True
            if self.strikethrough_var.get():
                new_comp['strikethrough'] = True
            if self.obfuscated_var.get():
                new_comp['obfuscated'] = True

            if self.current_index is None:
                self.components.append(new_comp)
                self._refresh_listbox()
                new_idx = len(self.components) - 1
                self.listbox.selection_set(new_idx)
                self.current_index = new_idx
            else:
                self.components[self.current_index] = new_comp
                self._refresh_listbox()
                self.listbox.selection_set(self.current_index)
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(bc.get_lang_text("error.title"), str(e))

    def get_array_string(self):
        if not self.components:
            return ""
        cleaned = []
        for comp in self.components:
            item = {k: v for k, v in comp.items() if k != 'type'}
            cleaned.append(item)
        return json.dumps(cleaned, separators=(',', ':'))

    def get_components(self):
        return self.components