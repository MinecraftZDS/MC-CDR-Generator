import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class PotDecorationsWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.decorations = ["", "", "", ""]  # 索引0背面,1左面,2右面,3前面

        # 创建四个输入框
        sides = ["back", "left", "right", "front"]
        for i, side in enumerate(sides):
            tk.Label(self, text=bc.get_lang_text(f"pot_decorations.{side}")).pack(anchor='w', padx=5, pady=(5,0))
            entry = tk.Entry(self, width=40)
            entry.pack(fill='x', padx=5, pady=2)
            setattr(self, f"entry_{i}", entry)
            # 存储到列表以便后续获取
            if not hasattr(self, "entries"):
                self.entries = []
            self.entries.append(entry)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("pot_decorations.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        # 收集四个输入框的值，允许空字符串（空字符串表示无装饰）
        for i, entry in enumerate(self.entries):
            val = entry.get().strip()
            self.decorations[i] = val
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        # 构建列表，如果四个都是空，则不输出组件
        if all(v == "" for v in self.decorations):
            return ""
        # 过滤空字符串？按照原版，空字符串应该被视为无装饰？但列表中空字符串可能被允许，但最好省略空项？为了准确，保留空字符串，因为游戏可能期望固定四个元素。
        # 为了简化，直接输出四个字符串，空字符串就是 ""
        items = ','.join(f'"{v}"' for v in self.decorations)
        return f'pot_decorations=[{items}]'