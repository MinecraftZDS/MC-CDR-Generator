import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc
from affiliated.entity.public.air import AirWidget
from affiliated.entity.public.custom_name import CustomNameWidget
from affiliated.entity.public.custom_name_visible import CustomNameVisibleWidget
from affiliated.entity.public.fall_distance import FallDistanceWidget
from affiliated.entity.public.fire import FireWidget
from affiliated.entity.public.glowing import GlowingWidget
from affiliated.entity.public.has_visual_fire import HasVisualFireWidget
from affiliated.entity.public.invulnerable import InvulnerableWidget
from affiliated.entity.public.motion import MotionWidget
from affiliated.entity.public.no_gravity import NoGravityWidget
from affiliated.entity.public.on_ground import OnGroundWidget
from affiliated.entity.public.passengers import PassengersWidget
from affiliated.entity.public.portal_cooldown import PortalCooldownWidget
from affiliated.entity.public.pos import PosWidget
from affiliated.entity.public.rotation import RotationWidget
from affiliated.entity.public.silent import SilentWidget
from affiliated.entity.public.tags import TagsWidget
from affiliated.entity.public.ticks_frozen import TicksFrozenWidget
from affiliated.entity.public.uuid import UUIDWidget
from affiliated.entity.private.allay.duplication_cooldown import DuplicationCooldownWidget
from affiliated.entity.private.allay.inventory import InventoryWidget
from affiliated.entity.private.armadillo.scute_time import ScuteTimeWidget
from affiliated.entity.private.armadillo.state import StateWidget
from affiliated.entity.private.armor_stand.disabled_slots import DisabledSlotsWidget
from affiliated.entity.private.armor_stand.invisible import InvisibleWidget
from affiliated.entity.private.armor_stand.marker import MarkerWidget
from affiliated.entity.private.armor_stand.no_base_plate import NoBasePlateWidget
from affiliated.entity.private.armor_stand.pose import PoseWidget
from affiliated.entity.private.armor_stand.show_arms import ShowArmsWidget
from affiliated.entity.private.armor_stand.small import SmallWidget

class EntityNBTSelector(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.available_components = {
            # 作者注：公共nbt部分
            "Air": AirWidget,
            "CustomName": CustomNameWidget,
            "CustomNameVisible": CustomNameVisibleWidget,
            "FallDistance": FallDistanceWidget,
            "Fire": FireWidget,
            "Glowing": GlowingWidget,
            "HasVisualFire": HasVisualFireWidget,
            "Invulnerable": InvulnerableWidget,
            "Motion": MotionWidget,
            "NoGravity": NoGravityWidget,
            "OnGround": OnGroundWidget,
            "Passengers": PassengersWidget,
            "PortalCooldown": PortalCooldownWidget,
            "Pos": PosWidget,
            "Rotation": RotationWidget,
            "Silent": SilentWidget,
            "Tags": TagsWidget,
            "TicksFrozen": TicksFrozenWidget,
            "UUID": UUIDWidget,

            # 作者注：私有nbt部分
            "DuplicationCooldown": DuplicationCooldownWidget,    # 作者注：以下组件适用于实体minecraft: allay
            "Inventory": InventoryWidget,

            "ScuteTime": ScuteTimeWidget,    # 作者注：以下组件适用于实体minecraft: armadillo
            "State": StateWidget,

            "DisabledSlots": DisabledSlotsWidget,    # 作者注：以下组件适用于实体minecraft: armor_stand
            "Invisible": InvisibleWidget,
            "Marker": MarkerWidget,
            "NoBasePlate": NoBasePlateWidget,
            "Pose": PoseWidget,
            "ShowArms": ShowArmsWidget,
            "Small": SmallWidget,
        }

        self.added_components = {}
        self.current_name = None
        self.current_widget = None

        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', pady=(0,5))

        tk.Label(top_frame, text=bc.get_lang_text("dropdown.select_entity_nbt")).pack(side='left')
        self.combo = ttk.Combobox(top_frame, values=list(self.available_components.keys()),
                                  state='readonly', width=25)
        self.combo.pack(side='left', padx=5)
        if self.available_components:
            self.combo.current(0)

        self.add_btn = ttk.Button(top_frame, text=bc.get_lang_text("button.add_entity_nbt"),
                                  command=self._add_current)
        self.add_btn.pack(side='left')

        mid_frame = tk.Frame(self)
        mid_frame.pack(fill='both', expand=True, pady=5)

        tk.Label(mid_frame, text=bc.get_lang_text("textbox.added_entity_nbt")).pack(anchor='w')
        self.listbox = tk.Listbox(mid_frame, height=6)
        self.listbox.pack(fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        self.config_frame = tk.Frame(self, relief='sunken', bd=1, height=250)
        self.config_frame.pack(fill='x', pady=5)
        self.config_frame.pack_propagate(False)

        self.placeholder = tk.Label(self.config_frame, text=bc.get_lang_text("entity.placeholder"))
        self.placeholder.pack(fill='both', expand=True)

    def _add_current(self):
        name = self.combo.get()
        if not name:
            return
        if name in self.added_components:
            messagebox.showerror(bc.get_lang_text("msgbox.error.duplicated"),
                                 bc.get_lang_text("msgbox.error.duplicated_format").format(name=name))
            return
        widget_class = self.available_components[name]
        widget = widget_class(self.config_frame)
        widget.pack(fill='both', expand=True)
        widget.pack_forget()  # 先隐藏
        self.added_components[name] = widget
        self.listbox.insert(tk.END, name)
        messagebox.showinfo(bc.get_lang_text("msgbox.info.added_entity_nbt"),
                            bc.get_lang_text("msgbox.info.added_entity_nbt_format").format(name=name))

    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        name = self.listbox.get(sel[0])
        if name == self.current_name:
            return
        if self.current_widget:
            self.current_widget.pack_forget()
        self.current_widget = self.added_components[name]
        self.current_widget.pack(fill='both', expand=True)
        self.current_name = name

    def get_combined_nbt(self):
        parts = []
        for widget in self.added_components.values():
            nbt = widget.get_nbt()
            if nbt:
                parts.append(nbt)
        if not parts:
            return ""
        return "{" + ",".join(parts) + "}"