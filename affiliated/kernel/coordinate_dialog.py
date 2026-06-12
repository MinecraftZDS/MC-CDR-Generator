import tkinter as tk
from tkinter import ttk
import affiliated.kernel.basic_components as bc

class CoordinateDialog:
    def __init__(self, parent, initial_coord=""):
        self.parent = parent
        self.result = initial_coord
        self.dialog = None
        self.axes = ['x', 'y', 'z']
        self.mode_vars = {}
        self.value_entries = {}
        self.facing_mode = False

    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(bc.get_lang_text("coordinate.dialog_title"))
        self.dialog.geometry("600x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        for i, axis in enumerate(self.axes):
            frame = tk.Frame(self.dialog, relief='groove', bd=1)
            frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

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

        if self.result:
            self._parse_coord(self.result)

        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=bc.get_lang_text("coordinate.ok"), command=self._ok).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=bc.get_lang_text("coordinate.cancel"), command=self._cancel).pack(side='left', padx=5)

        self.dialog.wait_window()
        return self.result

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

    def _parse_coord(self, coord_str):
        parts = coord_str.strip().split()
        if len(parts) != 3:
            return
        for idx, axis in enumerate(self.axes):
            part = parts[idx]
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

    def _update_facing_mode(self):
        any_facing = any(self.mode_vars[ax].get() == "relative_facing" for ax in self.axes)
        self.facing_mode = any_facing

    def _get_coord_string(self):
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
                coords.append(f"~{val}" if val else "~0")
            else:
                coords.append(f"^{val}" if val else "^0")
        return " ".join(coords)

    def _ok(self):
        self.result = self._get_coord_string()
        self.dialog.destroy()

    def _cancel(self):
        self.result = ""
        self.dialog.destroy()