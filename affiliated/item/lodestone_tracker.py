import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class LodestoneTrackerWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_target = {"dimension": "overworld", "pos": [0, 0, 0]}
        self.tracked = False

        # 维度下拉
        tk.Label(self, text=bc.get_lang_text("lodestone_tracker.dimension")).pack(anchor='w', padx=5, pady=2)
        dimensions = ["overworld", "the_nether", "the_end"]
        self.dim_combo = ttk.Combobox(self, values=dimensions, state='readonly', width=15)
        self.dim_combo.pack(anchor='w', padx=5, pady=2)
        self.dim_combo.current(0)

        # 坐标
        coord_frame = tk.Frame(self)
        coord_frame.pack(fill='x', padx=5, pady=2)
        tk.Label(coord_frame, text=bc.get_lang_text("lodestone_tracker.x")).pack(side='left', padx=2)
        self.x_entry = tk.Entry(coord_frame, width=8)
        self.x_entry.pack(side='left', padx=2)
        tk.Label(coord_frame, text="y").pack(side='left', padx=2)
        self.y_entry = tk.Entry(coord_frame, width=8)
        self.y_entry.pack(side='left', padx=2)
        tk.Label(coord_frame, text="z").pack(side='left', padx=2)
        self.z_entry = tk.Entry(coord_frame, width=8)
        self.z_entry.pack(side='left', padx=2)

        # tracked
        self.tracked_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text=bc.get_lang_text("lodestone_tracker.tracked"),
                       variable=self.tracked_var).pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("lodestone_tracker.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            dim = self.dim_combo.get().strip()
            x = int(self.x_entry.get().strip() or "0")
            y = int(self.y_entry.get().strip() or "0")
            z = int(self.z_entry.get().strip() or "0")
            tracked = self.tracked_var.get()
            self.current_target = {"dimension": dim, "pos": [x, y, z]}
            self.tracked = tracked
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("lodestone_tracker.error.invalid"))

    def get_nbt(self):
        return f'lodestone_tracker={{target:{{dimension:\
"{self.current_target["dimension"]}",pos:{self.current_target["pos"]}}},tracked:{str(self.tracked).lower()}}}'