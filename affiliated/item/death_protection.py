import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import traceback
import os
import affiliated.kernel.basic_components as bc

class DeathProtectionWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.effects = []          # 存储效果对象
        self.current_index = None

        # 布局
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- 左侧列表 ----------
        left_frame = tk.Frame(self, width=280)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(left_frame, text=bc.get_lang_text("death_protection.list_label")).grid(row=0, column=0, sticky='w')
        self.listbox = tk.Listbox(left_frame, height=12)
        self.listbox.grid(row=1, column=0, sticky='nsew', pady=5)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("death_protection.add"),
                   command=self._add_effect).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("button.remove_modifier"),
                   command=self._remove_current).pack(side='left', padx=5)

        # ---------- 右侧预览区 ----------
        right_frame = tk.Frame(self, relief='sunken', bd=1)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)

        # 预览区占位
        self.preview_frame = tk.Frame(right_frame)
        self.preview_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self._refresh_listbox()

    # ---------- 工具方法 ----------
    def _load_potion_effects(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, 'lists.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('potion_effects', [])
        except:
            return []

    # ---------- 列表管理 ----------
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, eff in enumerate(self.effects):
            typ = eff.get('type', 'unknown')
            display = f"{idx+1}: {typ}"
            if typ == 'apply_effects':
                cnt = len(eff.get('effects', []))
                display += f" ({cnt} sub-effects)"
            elif typ == 'remove_effects':
                cnt = len(eff.get('effects', []))
                display += f" ({cnt} IDs)"
            elif typ == 'teleport_randomly':
                display += f" diam={eff.get('diameter', 0)}"
            self.listbox.insert(tk.END, display)

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            self._clear_preview()
            return
        idx = sel[0]
        self.current_index = idx
        effect = self.effects[idx]
        self._display_effect(effect)

    def _clear_preview(self):
        for w in self.preview_frame.winfo_children():
            w.destroy()

    def _display_effect(self, effect):
        self._clear_preview()
        preview = ScrolledText(self.preview_frame, height=8, wrap='word', font=('Consolas',10))
        preview.pack(fill='both', expand=True, padx=5, pady=5)
        preview.insert('1.0', json.dumps(effect, indent=2))
        preview.config(state='disabled')
        btn = ttk.Button(self.preview_frame, text=bc.get_lang_text("death_protection.edit"),
                         command=lambda: self._open_effect_editor(effect))
        btn.pack(pady=5)

    def _add_effect(self):
        self._open_effect_editor(None)

    def _remove_current(self):
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
        self._clear_preview()
        if self.effects:
            self.listbox.selection_set(0)
            self._on_select()
        messagebox.showinfo(bc.get_lang_text("deleted.title"),
                            bc.get_lang_text("msg.deleted.modifier"))

    # ---------- 效果编辑器（二级窗口） ----------
    def _open_effect_editor(self, existing_effect):
        win = tk.Toplevel(self)
        win.title(bc.get_lang_text("death_protection.editor_title"))
        win.geometry("700x550")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text=bc.get_lang_text("death_protection.effect_type")).pack(anchor='w', padx=5, pady=5)
        effect_type_var = tk.StringVar(value="apply_effects")
        types = ["apply_effects", "remove_effects", "clear_all_effects", "teleport_randomly"]
        type_frame = tk.Frame(win)
        type_frame.pack(fill='x', padx=5)
        for t in types:
            rb = tk.Radiobutton(type_frame, text=t, variable=effect_type_var, value=t)
            rb.pack(side='left', padx=5)

        dynamic_frame = tk.Frame(win)
        dynamic_frame.pack(fill='both', expand=True, padx=5, pady=5)

        editor_data = {}

        def update_ui(*args):
            for w in dynamic_frame.winfo_children():
                w.destroy()
            etype = effect_type_var.get()
            if etype == "apply_effects":
                tk.Label(dynamic_frame, text=bc.get_lang_text("death_protection.sub_effects_list")).pack(anchor='w')
                listbox_frame = tk.Frame(dynamic_frame)
                listbox_frame.pack(fill='both', expand=True)
                sub_listbox = tk.Listbox(listbox_frame, height=12)
                sub_listbox.pack(side='left', fill='both', expand=True)
                scroll = tk.Scrollbar(listbox_frame, orient='vertical', command=sub_listbox.yview)
                scroll.pack(side='right', fill='y')
                sub_listbox.config(yscrollcommand=scroll.set)

                sub_effects = existing_effect.get('effects', []) if existing_effect and existing_effect.get('type') == 'apply_effects' else []

                def refresh_sublist():
                    sub_listbox.delete(0, tk.END)
                    for se in sub_effects:
                        display = f"{se.get('id','?')} amp:{se.get('amplifier',0)} dur:{se.get('duration',0)}"
                        sub_listbox.insert(tk.END, display)

                sub_btn_frame = tk.Frame(dynamic_frame)
                sub_btn_frame.pack(fill='x', pady=5)
                def add_sub():
                    self._edit_sub_effect(None, sub_effects, refresh_sublist, win)
                ttk.Button(sub_btn_frame, text=bc.get_lang_text("death_protection.add_sub"), command=add_sub).pack(side='left', padx=5)
                def edit_sub():
                    sel = sub_listbox.curselection()
                    if sel:
                        self._edit_sub_effect(sub_effects[sel[0]], sub_effects, refresh_sublist, win)
                ttk.Button(sub_btn_frame, text=bc.get_lang_text("death_protection.edit_sub"), command=edit_sub).pack(side='left', padx=5)
                def remove_sub():
                    sel = sub_listbox.curselection()
                    if sel:
                        del sub_effects[sel[0]]
                        refresh_sublist()
                ttk.Button(sub_btn_frame, text=bc.get_lang_text("button.remove_modifier"), command=remove_sub).pack(side='left', padx=5)

                refresh_sublist()
                editor_data['apply_effects'] = sub_effects

            elif etype == "remove_effects":
                tk.Label(dynamic_frame, text=bc.get_lang_text("death_protection.remove_ids_list")).pack(anchor='w')
                listbox_frame = tk.Frame(dynamic_frame)
                listbox_frame.pack(fill='both', expand=True)
                id_listbox = tk.Listbox(listbox_frame, height=12)
                id_listbox.pack(side='left', fill='both', expand=True)
                scroll = tk.Scrollbar(listbox_frame, orient='vertical', command=id_listbox.yview)
                scroll.pack(side='right', fill='y')
                id_listbox.config(yscrollcommand=scroll.set)

                remove_ids = existing_effect.get('effects', []) if existing_effect and existing_effect.get('type') == 'remove_effects' else []

                def refresh_ids():
                    id_listbox.delete(0, tk.END)
                    for eid in remove_ids:
                        id_listbox.insert(tk.END, eid)

                potion_effects = self._load_potion_effects()
                id_btn_frame = tk.Frame(dynamic_frame)
                id_btn_frame.pack(fill='x', pady=5)
                self.id_combo = ttk.Combobox(id_btn_frame, values=potion_effects, state='readonly', width=30)
                self.id_combo.pack(side='left', padx=5)
                def add_id():
                    val = self.id_combo.get().strip()
                    if val and val not in remove_ids:
                        remove_ids.append(val)
                        refresh_ids()
                ttk.Button(id_btn_frame, text=bc.get_lang_text("death_protection.add_id"), command=add_id).pack(side='left', padx=5)
                def remove_id():
                    sel = id_listbox.curselection()
                    if sel:
                        del remove_ids[sel[0]]
                        refresh_ids()
                ttk.Button(dynamic_frame, text=bc.get_lang_text("button.remove_modifier"), command=remove_id).pack(pady=5)

                refresh_ids()
                editor_data['remove_effects'] = remove_ids

            elif etype == "teleport_randomly":
                tk.Label(dynamic_frame, text=bc.get_lang_text("death_protection.diameter")).pack(anchor='w')
                diam_var = tk.StringVar(value=str(existing_effect.get('diameter', 0.0)) if existing_effect else "0.0")
                diam_entry = tk.Entry(dynamic_frame, textvariable=diam_var, width=10)
                diam_entry.pack(anchor='w')
                editor_data['teleport'] = diam_var

            else:  # clear_all_effects
                tk.Label(dynamic_frame, text=bc.get_lang_text("death_protection.clear_all_hint")).pack(anchor='w')

        effect_type_var.trace('w', update_ui)
        update_ui()

        def save():
            etype = effect_type_var.get()
            new_effect = {"type": etype}
            try:
                if etype == "apply_effects":
                    new_effect["effects"] = editor_data.get('apply_effects', [])
                elif etype == "remove_effects":
                    new_effect["effects"] = editor_data.get('remove_effects', [])
                elif etype == "teleport_randomly":
                    diam = float(editor_data['teleport'].get().strip())
                    if diam < 0:
                        raise ValueError
                    new_effect["diameter"] = diam
            except Exception as e:
                messagebox.showerror(bc.get_lang_text("error.title"), str(e))
                return

            if existing_effect is None:
                self.effects.append(new_effect)
            else:
                idx = self.effects.index(existing_effect)
                self.effects[idx] = new_effect
            self._refresh_listbox()
            win.destroy()
            messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))

        ttk.Button(win, text=bc.get_lang_text("death_protection.save_effect"), command=save).pack(pady=10)

    # ---------- 编辑子效果（apply_effects 内部） ----------
    def _edit_sub_effect(self, sub_effect, sub_list, refresh_callback, parent_win):
        dlg = tk.Toplevel(parent_win)
        dlg.title(bc.get_lang_text("death_protection.sub_effect_title"))
        dlg.geometry("500x500")
        dlg.transient(parent_win)
        dlg.grab_set()

        potion_effects = self._load_potion_effects()

        row = 0
        tk.Label(dlg, text="id").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        id_combo = ttk.Combobox(dlg, values=potion_effects, state='readonly', width=30)
        id_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        tk.Label(dlg, text="duration").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        duration_var = tk.StringVar()
        tk.Entry(dlg, textvariable=duration_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        tk.Label(dlg, text="amplifier").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        amp_var = tk.StringVar()
        tk.Entry(dlg, textvariable=amp_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        tk.Label(dlg, text="ambient").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        ambient_var = tk.BooleanVar()
        tk.Checkbutton(dlg, variable=ambient_var).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        tk.Label(dlg, text="show_icon").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        icon_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dlg, variable=icon_var).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        tk.Label(dlg, text="show_particles").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        part_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dlg, variable=part_var).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        if sub_effect:
            id_combo.set(sub_effect.get('id', ''))
            duration_var.set(str(sub_effect.get('duration', 0)))
            amp_var.set(str(sub_effect.get('amplifier', 0)))
            ambient_var.set(sub_effect.get('ambient', False))
            icon_var.set(sub_effect.get('show_icon', True))
            part_var.set(sub_effect.get('show_particles', True))
        else:
            duration_var.set("0")
            amp_var.set("0")
            ambient_var.set(False)
            icon_var.set(True)
            part_var.set(True)

        def save_sub():
            try:
                new_sub = {
                    "id": id_combo.get().strip(),
                    "duration": int(duration_var.get()),
                    "amplifier": int(amp_var.get()),
                    "ambient": ambient_var.get(),
                    "show_icon": icon_var.get(),
                    "show_particles": part_var.get()
                }
                if not new_sub['id']:
                    raise ValueError("ID cannot be empty")
                if sub_effect is None:
                    sub_list.append(new_sub)
                else:
                    idx = sub_list.index(sub_effect)
                    sub_list[idx] = new_sub
                refresh_callback()
                dlg.destroy()
                messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))
            except Exception as e:
                messagebox.showerror(bc.get_lang_text("error.title"), str(e))

        ttk.Button(dlg, text="OK", command=save_sub).grid(row=row, column=0, columnspan=2, pady=10)
        dlg.grid_columnconfigure(1, weight=1)

    # ---------- NBT 生成 ----------
    def get_nbt(self):
        if not self.effects:
            return ""
        return f'death_protection={{death_effects:{json.dumps(self.effects, separators=(",", ":"))}}}'