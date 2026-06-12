import tkinter as tk
from tkinter import ttk
import affiliated.kernel.basic_components as bc
from affiliated.kernel.text_components import TextComponentsManager

class CustomNameWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 嵌入文本组件管理器
        self.text_mgr = TextComponentsManager(self)

    def get_nbt(self):
        arr_str = self.text_mgr.get_array_string()
        if not arr_str:
            return ""
        return f'custom_name={arr_str}'