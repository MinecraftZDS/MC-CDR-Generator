import tkinter as tk
from tkinter import ttk, messagebox
from affiliated.kernel.text_components import TextComponentsManager
import affiliated.kernel.basic_components as bc

class InstrumentWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.current_data = {
            "description": [],
            "sound_event": {"range": 0.0, "sound_id": ""},
            "range": 0.0,
            "use_duration": 0
        }

        # 使用 notebook 组织布局
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # 选项卡：描述文本组件
        desc_frame = ttk.Frame(notebook)
        notebook.add(desc_frame, text=bc.get_lang_text("instrument.tab_description"))
        self.desc_mgr = TextComponentsManager(desc_frame)

        # 选项卡：sound_event
        sound_frame = ttk.Frame(notebook)
        notebook.add(sound_frame, text=bc.get_lang_text("instrument.tab_sound"))

        tk.Label(sound_frame, text=bc.get_lang_text("instrument.sound_id")).pack(anchor='w', padx=5, pady=2)
        self.sound_id_entry = tk.Entry(sound_frame, width=40)
        self.sound_id_entry.pack(fill='x', padx=5, pady=2)

        tk.Label(sound_frame, text=bc.get_lang_text("instrument.sound_range")).pack(anchor='w', padx=5, pady=2)
        self.sound_range_entry = tk.Entry(sound_frame, width=10)
        self.sound_range_entry.pack(anchor='w', padx=5, pady=2)

        # 选项卡：顶层 range 和 use_duration
        other_frame = ttk.Frame(notebook)
        notebook.add(other_frame, text=bc.get_lang_text("instrument.tab_other"))

        tk.Label(other_frame, text=bc.get_lang_text("instrument.range")).pack(anchor='w', padx=5, pady=2)
        self.range_entry = tk.Entry(other_frame, width=10)
        self.range_entry.pack(anchor='w', padx=5, pady=2)

        tk.Label(other_frame, text=bc.get_lang_text("instrument.use_duration")).pack(anchor='w', padx=5, pady=2)
        self.duration_entry = tk.Entry(other_frame, width=10)
        self.duration_entry.pack(anchor='w', padx=5, pady=2)

        # 保存按钮
        self.save_btn = ttk.Button(self, text=bc.get_lang_text("instrument.save"),
                                   command=self._save)
        self.save_btn.pack(pady=10)

        self._save(silent=True)

    def _save(self, silent=False):
        try:
            desc_list = self.desc_mgr.get_components()
            sound_id = self.sound_id_entry.get().strip()
            sound_range = float(self.sound_range_entry.get().strip() or "0.0")
            outer_range = float(self.range_entry.get().strip() or "0.0")
            use_duration = int(self.duration_entry.get().strip() or "0")
            if use_duration < 0:
                raise ValueError

            self.current_data = {
                "description": desc_list,
                "sound_event": {"range": sound_range, "sound_id": sound_id},
                "range": outer_range,
                "use_duration": use_duration
            }
            if not silent:
                messagebox.showinfo(bc.get_lang_text("success.title"),
                                    bc.get_lang_text("msgbox.info.saved"))
        except:
            if not silent:
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("instrument.error.invalid"))

    def get_nbt(self):
        # 仅当有有效数据时才输出
        if not self.current_data["description"] and not self.current_data["sound_event"]["sound_id"]:
            return ""
        import json
        obj = {
            "description": self.current_data["description"],
            "sound_event": self.current_data["sound_event"],
            "range": self.current_data["range"],
            "use_duration": self.current_data["use_duration"]
        }
        # 移除空字段（可选）
        if not obj["sound_event"]["sound_id"]:
            del obj["sound_event"]
        if obj["range"] == 0.0:
            del obj["range"]   # 可选，根据需求
        # 输出 instrument={...}
        return f'instrument={json.dumps(obj, separators=(",", ":"))}'