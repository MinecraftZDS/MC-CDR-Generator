import tkinter as tk
from tkinter import ttk
import affiliated.kernel.basic_components as bc

class CoordinateEditor(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='x', expand=False)

        self.axes = ['x', 'y', 'z']
        self.mode_vars = {}
        self.value_entries = {}

        self.facing_mode = False

        for i, axis in enumerate(self.axes):
            frame = tk.Frame(self, relief='groove', bd=1)
            frame.pack(side='left', fill='both', expand=True, padx=2, pady=2)

            tk.Label(frame, text=axis.upper(), font=('Arial', 10, 'bold')).pack(pady=2)

            mode_var = tk.StringVar(value="absolute")
            self.mode_vars[axis] = mode_var
            rb_abs = tk.Radiobutton(frame, text=bc.get_lang_text("coordinate.absolute"),
                                    variable=mode_var, value="absolute")
            rb_rel_pos = tk.Radiobutton(frame, text=bc.get_lang_text("coordinate.relative_pos"),
                                        variable=mode_var, value="relative_pos")
            rb_rel_facing = tk.Radiobutton(frame, text=bc.get_lang_text("coordinate.relative_facing"),
                                           variable=mode_var, value="relative_facing")
            rb_abs.pack(anchor='w')
            rb_rel_pos.pack(anchor='w')
            rb_rel_facing.pack(anchor='w')

            entry = tk.Entry(frame, width=8)
            entry.pack(pady=2)
            self.value_entries[axis] = entry

            mode_var.trace('w', lambda *args, ax=axis: self._on_mode_change(ax))

        self._update_facing_mode()

    def _on_mode_change(self, axis):
        new_mode = self.mode_vars[axis].get()
        if new_mode == "relative_facing":
            if not self.facing_mode:
                self.facing_mode = True
                for ax in self.axes:
                    if ax != axis:
                        self.mode_vars[ax].set("relative_facing")
        else:
            if self.facing_mode:
                self.facing_mode = False
                for ax in self.axes:
                    if ax != axis:
                        self.mode_vars[ax].set("absolute")
                self.mode_vars[axis].set(new_mode)

    def _update_facing_mode(self):
        any_facing = any(self.mode_vars[ax].get() == "relative_facing" for ax in self.axes)
        self.facing_mode = any_facing

    def get_coordinate_nbt(self):
        coords = []
        for axis in self.axes:
            mode = self.mode_vars[axis].get()
            val = self.value_entries[axis].get().strip()
            if mode == "absolute":
                if val == "":
                    coords.append("0")
                else:
                    try:
                        num = float(val)
                        if num.is_integer():
                            coords.append(str(int(num)))
                        else:
                            coords.append(f"{num:.2f}".rstrip('0').rstrip('.'))
                    except:
                        coords.append(val)
            elif mode == "relative_pos":
                if val == "":
                    coords.append("~0")
                else:
                    coords.append(f"~{val}")
            else:  # relative_facing
                if val == "":
                    coords.append("^0")
                else:
                    coords.append(f"^{val}")
        return f"[{','.join(coords)}]"

    def set_coordinate_from_nbt(self, coord_str):
        stripped = coord_str.strip('[]')
        parts = stripped.split(',')
        if len(parts) != 3:
            return
        for idx, axis in enumerate(self.axes):
            part = parts[idx].strip()
            if part.startswith('^'):
                mode = "relative_facing"
                val = part[1:]
            elif part.startswith('~'):
                mode = "relative_pos"
                val = part[1:]
            else:
                mode = "absolute"
                val = part
            self.mode_vars[axis].set(mode)
            self.value_entries[axis].delete(0, tk.END)
            self.value_entries[axis].insert(0, val)
        self._update_facing_mode()

    def clear(self):
        for axis in self.axes:
            self.mode_vars[axis].set("absolute")
            self.value_entries[axis].delete(0, tk.END)
        self.facing_mode = False