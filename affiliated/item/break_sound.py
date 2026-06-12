import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class BreakSoundWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_sound = ""

        # 标签
        tk.Label(self, text=bc.get_lang_text("break_sound.label")).pack(anchor='w', padx=5, pady=(10, 0))

        # 输入框
        self.sound_entry = tk.Entry(self, width=50)
        self.sound_entry.pack(fill='x', padx=5, pady=5)

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("break_sound.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        # 初始化静默保存
        self._save(silent=True)

    def _save(self, silent=False):
        sound = self.sound_entry.get().strip()
        if not sound:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("break_sound.error.empty"))
            return
        self.current_sound = sound
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_sound:
            return ""
        return f'minecraft:break_sound={{sound_id:"{self.current_sound}"}}'