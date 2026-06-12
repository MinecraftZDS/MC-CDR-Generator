import tkinter as tk
from tkinter import ttk
import affiliated.kernel.basic_components as bc

def add_command_controls(parent):
    bottom_frame = tk.Frame(parent)
    bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    preview_label = tk.Label(bottom_frame, text=bc.get_lang_text("button.command.preview"))
    preview_label.pack(anchor='w')

    preview_text = tk.Text(bottom_frame, height=6, state='disabled', wrap='word', font=('Consolas', 10))
    preview_text.pack(fill='x', pady=(0, 5))

    btn_frame = tk.Frame(bottom_frame)
    btn_frame.pack(anchor='w')

    generate_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.command.generate"))
    generate_btn.pack(side='left', padx=(0, 5))

    copy_btn = ttk.Button(btn_frame, text=bc.get_lang_text("button.copycmd"))
    copy_btn.pack(side='left')

    return preview_text, generate_btn, copy_btn
