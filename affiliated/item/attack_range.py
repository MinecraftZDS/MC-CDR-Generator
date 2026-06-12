# affiliated/attack_range.py
import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc

class AttackRangeWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._saved_nbt = ""

        fields = [
            ("min_reach", "min.reach", 0, 64, int),
            ("max_reach", "max.reach", 0, 64, int),
            ("min_creative_reach", "min.creative.reach", 0, 64, int),
            ("max_creative_reach", "max.creative.reach", 0, 64, int),
            ("hitbox_margin", "hitbox.margin", 0, 1, float),
            ("mob_factor", "mob.factor", 0, 2, float)
        ]
        self.entries = {}

        row = 0
        for key, suffix, min_val, max_val, data_type in fields:
            label = tk.Label(self, text=bc.get_lang_text(f"inputbox.{suffix}"))
            label.grid(row=row, column=0, sticky='w', padx=5, pady=2)

            var = tk.StringVar(value=str(min_val))
            entry = tk.Entry(self, textvariable=var, width=8)
            entry.grid(row=row, column=1, padx=5, pady=2)
            self.entries[key] = (var, data_type, min_val, max_val)

            row += 1

        self.save_btn = ttk.Button(self, text=bc.get_lang_text("button.save.attackrange"),
                           command=lambda: self._save_config(silent=False))
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=5)

        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.grid(row=row+1, column=0, columnspan=2)

        self._save_config(silent=True)

    def _save_config(self, silent=False):
        nbt_parts = []
        valid = True
        for key, (var, data_type, min_val, max_val) in self.entries.items():
            raw = var.get().strip()
            if not raw:
                valid = False
                break
            try:
                if data_type == int:
                    val = int(float(raw))
                else:
                    val = float(raw)
                if val < min_val or val > max_val:
                    valid = False
                    break
                if data_type == int:
                    nbt_parts.append(f"{key}:{val}")
                else:
                    formatted = f"{val:.2f}".rstrip('0').rstrip('.') if val != int(val) else str(int(val))
                    nbt_parts.append(f"{key}:{formatted}")
            except ValueError:
                valid = False
                break
        if valid:
            self._saved_nbt = f"attack_range={{{', '.join(nbt_parts)}}}"
            if not silent:
                messagebox.showinfo(bc.get_lang_text("msgbox.info.saved"), "Configuration saved.")
        else:
            if not silent:
                messagebox.showerror("Error", "Invalid values. Please check the input ranges.")
            else:
                # 静默模式下，清空之前保存的 NBT
                self._saved_nbt = ""

    def get_nbt(self):
        return self._saved_nbt