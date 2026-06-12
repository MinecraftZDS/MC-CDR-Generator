import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class ContainerLootWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_loot_table = ""
        self.current_seed = 0.0

        tk.Label(self, text=bc.get_lang_text("container_loot.loot_table")).pack(anchor='w', padx=5, pady=(10, 0))
        self.loot_table_entry = tk.Entry(self, width=50)
        self.loot_table_entry.pack(fill='x', padx=5, pady=2)

        tk.Label(self, text=bc.get_lang_text("container_loot.seed")).pack(anchor='w', padx=5, pady=(5, 0))
        self.seed_entry = tk.Entry(self, width=20)
        self.seed_entry.pack(anchor='w', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("container_loot.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        loot_table = self.loot_table_entry.get().strip()
        seed_str = self.seed_entry.get().strip()

        if not loot_table:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("container_loot.error.loot_table_empty"))
            return

        if not seed_str:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("container_loot.error.seed_empty"))
            return

        try:
            seed = float(seed_str)
        except ValueError:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("container_loot.error.seed_invalid"))
            return

        # 范围验证： -2147483649 < seed < 2147483648
        if seed <= -2147483649 or seed >= 2147483648:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("container_loot.error.seed_range"))
            return

        self.current_loot_table = loot_table
        self.current_seed = seed

        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_loot_table:
            return ""
        # 格式化种子：如果是整数则输出整数形式，否则输出浮点数（保留足够精度）
        seed_val = self.current_seed
        if seed_val.is_integer():
            seed_str = str(int(seed_val))
        else:
            # 使用 repr 避免科学计数法，但可能末尾有 .0 ？已经处理整数情况
            seed_str = f"{seed_val:.10f}".rstrip('0').rstrip('.')  # 去掉末尾多余0
        return f'container_loot={{loot_table:"{self.current_loot_table}",seed:{seed_str}}}'