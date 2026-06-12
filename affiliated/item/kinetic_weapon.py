import tkinter as tk
from tkinter import ttk, messagebox
import json
import affiliated.kernel.basic_components as bc

class KineticWeaponWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 数据存储
        self.delay_tick = 0
        self.forward_movement = None
        self.conditions = {
            "dismount_conditions": {"min_speed": 0.0, "min_relative_speed": 0.0},
            "max_durations_ticks": {"min_speed": 0.0, "min_relative_speed": 0.0},
            "damage_conditions": {"min_speed": 0.0, "min_relative_speed": 0.0}
        }
        self.contact_cooldown_ticks = 1

        # 布局
        self.grid_columnconfigure(1, weight=1)

        row = 0
        # delay_tick
        tk.Label(self, text=bc.get_lang_text("kinetic_weapon.delay_tick")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.delay_entry = tk.Entry(self, width=10)
        self.delay_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        self.delay_entry.insert(0, "0")
        row += 1

        # forward_movement 可选
        self.forward_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("kinetic_weapon.forward_movement_enable"),
                       variable=self.forward_var, command=self._toggle_forward).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        row += 1
        tk.Label(self, text=bc.get_lang_text("kinetic_weapon.forward_movement")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.forward_entry = tk.Entry(self, width=10, state='disabled')
        self.forward_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1

        # 三个标签页
        notebook = ttk.Notebook(self)
        notebook.grid(row=row, column=0, columnspan=2, sticky='nsew', pady=5)
        self.grid_rowconfigure(row, weight=1)
        row += 1

        # 为每个条件创建标签页，内部水平排列两个输入框
        self.tab_entries = {}
        for key in ["dismount_conditions", "max_durations_ticks", "damage_conditions"]:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=bc.get_lang_text(f"kinetic_weapon.{key}"))
            frame = tk.Frame(tab)
            frame.pack(fill='x', padx=5, pady=5)
            tk.Label(frame, text=bc.get_lang_text("kinetic_weapon.min_speed")).pack(side='left', padx=5)
            min_entry = tk.Entry(frame, width=10)
            min_entry.pack(side='left', padx=5)
            min_entry.insert(0, "0.0")
            tk.Label(frame, text=bc.get_lang_text("kinetic_weapon.min_relative_speed")).pack(side='left', padx=5)
            rel_entry = tk.Entry(frame, width=10)
            rel_entry.pack(side='left', padx=5)
            rel_entry.insert(0, "0.0")
            self.tab_entries[key] = {"min_speed": min_entry, "min_relative_speed": rel_entry}

        # contact_cooldown_ticks
        tk.Label(self, text=bc.get_lang_text("kinetic_weapon.contact_cooldown_ticks")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.cooldown_entry = tk.Entry(self, width=10)
        self.cooldown_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        self.cooldown_entry.insert(0, "1")
        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("kinetic_weapon.save"),
                                   command=self._save)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        self._toggle_forward()
        self._save(silent=True)

    def _toggle_forward(self):
        if self.forward_var.get():
            self.forward_entry.config(state='normal')
        else:
            self.forward_entry.config(state='disabled')
            self.forward_entry.delete(0, tk.END)

    def _save(self, silent=False):
        try:
            # delay_tick
            delay_str = self.delay_entry.get().strip()
            if not delay_str:
                delay_str = "0"
            delay = int(delay_str)
            if delay < 0:
                raise ValueError("delay_tick < 0")
            self.delay_tick = delay

            # forward_movement
            if self.forward_var.get():
                fwd_str = self.forward_entry.get().strip()
                if not fwd_str:
                    raise ValueError("forward_movement is empty")
                fwd = int(fwd_str)
                if fwd < 0:
                    raise ValueError("forward_movement < 0")
                self.forward_movement = fwd
            else:
                self.forward_movement = None

            # 三个标签页的数据
            for key, entries in self.tab_entries.items():
                min_speed_str = entries["min_speed"].get().strip()
                min_rel_str = entries["min_relative_speed"].get().strip()
                if not min_speed_str:
                    min_speed_str = "0.0"
                if not min_rel_str:
                    min_rel_str = "0.0"
                min_speed = float(min_speed_str)
                min_rel = float(min_rel_str)
                if min_speed < 0 or min_rel < 0:
                    raise ValueError(f"{key} values negative")
                self.conditions[key] = {"min_speed": min_speed, "min_relative_speed": min_rel}

            # contact_cooldown_ticks
            cool_str = self.cooldown_entry.get().strip()
            if not cool_str:
                cool_str = "1"
            cooldown = int(cool_str)
            if cooldown <= 0:
                raise ValueError("contact_cooldown_ticks <= 0")
            self.contact_cooldown_ticks = cooldown

            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))

        except ValueError as e:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     f"Invalid input: {str(e)}")
        except Exception as e:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     f"Unexpected error: {str(e)}")

    def get_nbt(self):
        obj = {
            "delay_tick": self.delay_tick,
            "dismount_conditions": self.conditions["dismount_conditions"],
            "max_durations_ticks": self.conditions["max_durations_ticks"],
            "damage_conditions": self.conditions["damage_conditions"],
            "contact_cooldown_ticks": self.contact_cooldown_ticks
        }
        if self.forward_movement is not None:
            obj["forward_movement"] = self.forward_movement

        return f'kinetic_weapon={json.dumps(obj, separators=(",", ":"))}'