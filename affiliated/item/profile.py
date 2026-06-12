import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc
from affiliated.kernel.player_skin_viewer import PlayerSkinViewer

class ProfileWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_name = ""

        # 输入框和保存按钮
        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(top_frame, text=bc.get_lang_text("profile.input_label")).pack(side='left')
        self.name_entry = tk.Entry(top_frame, width=25)
        self.name_entry.pack(side='left', padx=5)
        self.save_btn = ttk.Button(top_frame, text=bc.get_lang_text("profile.save"),
                                   command=self._save)
        self.save_btn.pack(side='left')
        self.preview_btn = ttk.Button(top_frame, text=bc.get_lang_text("profile.preview"),
                                      command=self._preview)
        self.preview_btn.pack(side='left', padx=5)

        # 皮肤预览器
        self.viewer = PlayerSkinViewer(self)

    def _save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("profile.error.empty"))
            return
        self.current_name = name
        messagebox.showinfo(bc.get_lang_text("success.title"),
                            bc.get_lang_text("msgbox.info.saved"))

    def _preview(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror(bc.get_lang_text("error.title"),
                                 bc.get_lang_text("profile.error.empty"))
            return
        self.viewer.query_and_display(name)

    def get_nbt(self):
        if not self.current_name:
            return ""
        return f'profile="{self.current_name}"'