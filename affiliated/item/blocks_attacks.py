import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class BlocksAttacksWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_data = {}

        # 使用 grid 布局
        self.grid_columnconfigure(0, weight=0)  # 标签列
        self.grid_columnconfigure(1, weight=1)  # 输入列

        row = 0
        # block_delay_seconds (非负整数)
        tk.Label(self, text=bc.get_lang_text("blocks_attacks.block_delay_seconds")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.delay_entry = tk.Entry(self, width=20)
        self.delay_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # disable_cooldown_scale (非负浮点数)
        tk.Label(self, text=bc.get_lang_text("blocks_attacks.disable_cooldown_scale")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.cooldown_entry = tk.Entry(self, width=20)
        self.cooldown_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        row += 1

        # item_damage 分组框
        damage_frame = ttk.LabelFrame(self, text=bc.get_lang_text("blocks_attacks.item_damage"))
        damage_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        damage_frame.columnconfigure(1, weight=1)
        row_inner = 0

        # base
        tk.Label(damage_frame, text=bc.get_lang_text("blocks_attacks.base")).grid(row=row_inner, column=0, sticky='w', padx=5, pady=2)
        self.base_entry = tk.Entry(damage_frame, width=20)
        self.base_entry.grid(row=row_inner, column=1, sticky='ew', padx=5, pady=2)
        row_inner += 1

        # factor
        tk.Label(damage_frame, text=bc.get_lang_text("blocks_attacks.factor")).grid(row=row_inner, column=0, sticky='w', padx=5, pady=2)
        self.factor_entry = tk.Entry(damage_frame, width=20)
        self.factor_entry.grid(row=row_inner, column=1, sticky='ew', padx=5, pady=2)
        row_inner += 1

        # threshold
        tk.Label(damage_frame, text=bc.get_lang_text("blocks_attacks.threshold")).grid(row=row_inner, column=0, sticky='w', padx=5, pady=2)
        self.threshold_entry = tk.Entry(damage_frame, width=20)
        self.threshold_entry.grid(row=row_inner, column=1, sticky='ew', padx=5, pady=2)

        row += 1

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("blocks_attacks.save"),
                                   command=self._save)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # 初始化静默保存
        self._save(silent=True)

    def _save(self, silent=False):
        try:
            delay = float(self.delay_entry.get().strip()) if self.delay_entry.get().strip() else 0.0
            if delay < 0:
                raise ValueError
            cooldown = float(self.cooldown_entry.get().strip()) if self.cooldown_entry.get().strip() else 0.0
            if cooldown < 0:
                raise ValueError
            base = float(self.base_entry.get().strip()) if self.base_entry.get().strip() else 0.0
            factor = float(self.factor_entry.get().strip()) if self.factor_entry.get().strip() else 0.0
            threshold = float(self.threshold_entry.get().strip()) if self.threshold_entry.get().strip() else 0.0

            self.current_data = {
                "block_delay_seconds": delay,
                "disable_cooldown_scale": cooldown,
                "item_damage": {
                    "base": base,
                    "factor": factor,
                    "threshold": threshold
                }
            }

            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except ValueError:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("blocks_attacks.error.invalid_number"))

    def get_nbt(self):
        if not self.current_data:
            return ""
        damage = self.current_data["item_damage"]
        return f'blocks_attacks={{block_delay_seconds:{self.current_data["block_delay_seconds"]},disable_cooldown_scale:{self.current_data["disable_cooldown_scale"]},item_damage:{{base:{damage["base"]},factor:{damage["factor"]},threshold:{damage["threshold"]}}}}}'