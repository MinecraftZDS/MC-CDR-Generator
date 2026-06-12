import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class NoteBlockSoundWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_sound = ""

        tk.Label(self, text=bc.get_lang_text("note_block_sound.label")).pack(anchor='w', padx=5, pady=(10, 0))
        self.sound_entry = tk.Entry(self, width=30)
        self.sound_entry.pack(fill='x', padx=5, pady=2)

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("note_block_sound.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        val = self.sound_entry.get().strip()
        if not val:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("note_block_sound.error.empty"))
            return
        self.current_sound = val
        if not silent:
            messagebox.showinfo(bc.get_lang_text("success.title"),
                                bc.get_lang_text("msgbox.info.saved"))

    def get_nbt(self):
        if not self.current_sound:
            return ""
        return f'note_block_sound="{self.current_sound}"'