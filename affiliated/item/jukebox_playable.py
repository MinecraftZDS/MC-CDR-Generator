import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class JukeboxPlayableWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_song = ""

        tk.Label(self, text=bc.get_lang_text("jukebox_playable.label")).pack(anchor='w', padx=5, pady=(10,0))
        self.entry = tk.Entry(self, width=50)
        self.entry.pack(fill='x', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("jukebox_playable.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        val = self.entry.get().strip()
        self.current_song = val
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_song:
            return ""
        return f'jukebox_playable="{self.current_song}"'