import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import affiliated.kernel.basic_components as bc

class BlockStateWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_states = ""

        # 使用 grid 布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # 文本框可伸缩

        # 标签
        tk.Label(self, text=bc.get_lang_text("block_state.label")).grid(row=0, column=0, sticky='w', padx=5, pady=(10, 0))

        # 多行文本框
        self.text_area = ScrolledText(self, height=8, wrap='word', font=('Consolas', 10))
        self.text_area.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("block_state.save"),
                                   command=self._save)
        self.save_btn.grid(row=2, column=0, pady=10)

        # 初始化静默保存
        self._save(silent=True)

    def _save(self, silent=False):
        states = self.text_area.get('1.0', 'end-1c').strip()
        self.current_states = states
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_states:
            return ""
        # 直接拼接 block_state={...}，用户需确保输入的内容是合法的方块状态字符串
        return f'block_state={{{self.current_states}}}'