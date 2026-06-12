import tkinter as tk
from tkinter import ttk, messagebox
import json
import affiliated.kernel.basic_components as bc

class PoseWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        # 存储每个部位的三轴角度
        self.parts = {
            "body": [0.0, 0.0, 0.0],
            "head": [0.0, 0.0, 0.0],
            "left_arm": [0.0, 0.0, 0.0],
            "left_leg": [0.0, 0.0, 0.0],
            "right_arm": [0.0, 0.0, 0.0],
            "right_leg": [0.0, 0.0, 0.0],
        }

        # 构建滚动区域
        canvas = tk.Canvas(self, highlightthickness=0)
        v_scroll = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        h_scroll = tk.Scrollbar(self, orient='horizontal', command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))

        row = 0
        self.entries = {}  # part_name -> [x_entry, y_entry, z_entry]
        for part in self.parts.keys():
            lbl = bc.get_lang_text(f"pose.{part}")
            frame = tk.Frame(inner)
            frame.pack(fill='x', padx=5, pady=2)
            tk.Label(frame, text=lbl, width=10, anchor='w').pack(side='left')
            x_entry = tk.Entry(frame, width=6)
            y_entry = tk.Entry(frame, width=6)
            z_entry = tk.Entry(frame, width=6)
            x_entry.pack(side='left', padx=2)
            y_entry.pack(side='left', padx=2)
            z_entry.pack(side='left', padx=2)
            self.entries[part] = (x_entry, y_entry, z_entry)
            # 默认值 0
            for e in (x_entry, y_entry, z_entry):
                e.insert(0, "0.0")

        self.save_btn = ttk.Button(inner, text=bc.get_lang_text("pose.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)
        self._save(silent=True)

    def _save(self, silent=False):
        try:
            for part, (x_e, y_e, z_e) in self.entries.items():
                x = float(x_e.get().strip() or "0.0")
                y = float(y_e.get().strip() or "0.0")
                z = float(z_e.get().strip() or "0.0")
                self.parts[part] = [x, y, z]
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"), bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"), bc.get_lang_text("pose.error.invalid"))

    def get_nbt(self):
        # 构建 Pose 对象
        pose_dict = {}
        for part, angles in self.parts.items():
            # 注意：部位名称映射为 Minecraft 标准键 (body, head, left_arm, left_leg, right_arm, right_leg)
            key = part  # 已匹配
            pose_dict[key] = angles
        return f'Pose:{json.dumps(pose_dict, separators=(",", ":"))}'