import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class FireworkExplosionWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_colors = 0
        self.has_trail = False
        self.has_twinkle = False
        self.shape = "small_ball"

        shapes = ["small_ball", "large_ball", "star", "creeper", "burst"]

        # 颜色（整数）
        tk.Label(self, text=bc.get_lang_text("firework.colors")).pack(anchor='w', padx=5, pady=(10,0))
        self.colors_entry = tk.Entry(self, width=10)
        self.colors_entry.pack(anchor='w', padx=5, pady=2)
        self.colors_entry.insert(0, "0")

        # 轨迹
        self.trail_var = tk.BooleanVar()
        tk.Checkbutton(self, text=bc.get_lang_text("firework.has_trail"),
                       variable=self.trail_var).pack(anchor='w', padx=5, pady=2)

        # 闪烁
        self.twinkle_var = tk.BooleanVar()
        tk.Checkbutton(self, text=bc.get_lang_text("firework.has_twinkle"),
                       variable=self.twinkle_var).pack(anchor='w', padx=5, pady=2)

        # 形状下拉
        tk.Label(self, text=bc.get_lang_text("firework.shape")).pack(anchor='w', padx=5, pady=2)
        self.shape_combo = ttk.Combobox(self, values=shapes, state='readonly', width=15)
        self.shape_combo.pack(anchor='w', padx=5, pady=2)
        self.shape_combo.current(0)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("firework.save_explosion"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            colors = int(self.colors_entry.get().strip())
        except:
            colors = 0
        trail = self.trail_var.get()
        twinkle = self.twinkle_var.get()
        shape = self.shape_combo.get()
        if shape not in ["small_ball", "large_ball", "star", "creeper", "burst"]:
            shape = "small_ball"

        self.current_colors = colors
        self.has_trail = trail
        self.has_twinkle = twinkle
        self.shape = shape

        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        # 颜色输出为数组，即使只有一个元素也用方括号
        return f'firework_explosion={{colors:[{self.current_colors}],has_trail:{str(self.has_trail).lower()},has_twinkle:{str(self.has_twinkle).lower()},shape:"{self.shape}"}}'