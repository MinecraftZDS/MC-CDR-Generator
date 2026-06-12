import tkinter as tk
from tkinter import ttk, messagebox
import affiliated.kernel.basic_components as bc
from affiliated.item.attack_range import AttackRangeWidget
from affiliated.item.attribute_modifier import AttributeModifierWidget
from affiliated.item.banner_patterns import BannerPatternsWidget
from affiliated.item.base_color import BaseColorWidget
from affiliated.item.bees import BeesWidget
from affiliated.item.block_entity_data import BlockEntityDataWidget
from affiliated.item.block_state import BlockStateWidget
from affiliated.item.blocks_attacks import BlocksAttacksWidget
from affiliated.item.break_sound import BreakSoundWidget
from affiliated.item.bucket_entity_data import BucketEntityDataWidget
from affiliated.item.bundle_contents import BundleContentsWidget
from affiliated.item.can_break import CanBreakWidget
from affiliated.item.can_place_on import CanPlaceOnWidget
from affiliated.item.charged_projectiles import ChargedProjectilesWidget
from affiliated.item.consumable import ConsumableWidget
from affiliated.item.container_loot import ContainerLootWidget
from affiliated.item.container import ContainerWidget
from affiliated.item.custom_data import CustomDataWidget
from affiliated.item.custom_name import CustomNameWidget
from affiliated.item.damage_resistant import DamageResistantWidget
from affiliated.item.damage_type import DamageTypeWidget
from affiliated.item.damage import DamageWidget
from affiliated.item.death_protection import DeathProtectionWidget
from affiliated.item.dye import DyeWidget
from affiliated.item.dyed_color import DyedColorWidget
from affiliated.item.enchantable import EnchantableWidget
from affiliated.item.enchantment_glint_override import EnchantmentGlintOverrideWidget
from affiliated.item.enchantments import EnchantmentsWidget
from affiliated.item.entity_data import EntityDataWidget
from affiliated.item.equippable import EquippableWidget
from affiliated.item.firework_explosion import FireworkExplosionWidget
from affiliated.item.fireworks import FireworksWidget
from affiliated.item.food import FoodWidget
from affiliated.item.glider import GliderWidget
from affiliated.item.instrument import InstrumentWidget
from affiliated.item.intangible_projectile import IntangibleProjectileWidget
from affiliated.item.item_model import ItemModelWidget
from affiliated.item.item_name import ItemNameWidget
from affiliated.item.jukebox_playable import JukeboxPlayableWidget
from affiliated.item.kinetic_weapon import KineticWeaponWidget
from affiliated.item.lock import LockWidget
from affiliated.item.lodestone_tracker import LodestoneTrackerWidget
from affiliated.item.lore import LoreWidget
from affiliated.item.map_color import MapColorWidget
from affiliated.item.map_id import MapIdWidget
from affiliated.item.max_damage import MaxDamageWidget
from affiliated.item.max_stack_size import MaxStackSizeWidget
from affiliated.item.minimum_attack_charge import MinimumAttackChargeWidget
from affiliated.item.note_block_sound import NoteBlockSoundWidget
from affiliated.item.ominous_bottle_amplifier import OminousBottleAmplifierWidget
from affiliated.item.piercing_weapon import PiercingWeaponWidget
from affiliated.item.pot_decorations import PotDecorationsWidget
from affiliated.item.potion_contents import PotionContentsWidget
from affiliated.item.potion_duration_scale import PotionDurationScaleWidget
from affiliated.item.profile import ProfileWidget
from affiliated.item.provides_banner_patterns import ProvidesBannerPatternsWidget
from affiliated.item.rarity import RarityWidget
from affiliated.item.recipes import RecipesWidget
from affiliated.item.repair_cost import RepairCostWidget
from affiliated.item.repairable import RepairableWidget
from affiliated.item.stored_enchantments import StoredEnchantmentsWidget
from affiliated.item.suspicious_stew_effects import SuspiciousStewEffectsWidget
from affiliated.item.tool import ToolWidget
from affiliated.item.tooltip_display import TooltipDisplayWidget
from affiliated.item.unbreakable import UnbreakableWidget
from affiliated.item.use_cooldown import UseCooldownWidget
from affiliated.item.use_effects import UseEffectsWidget
from affiliated.item.use_remainder import UseRemainderWidget
from affiliated.item.weapon import WeaponWidget
from affiliated.item.writable_book_content import WritableBookContentWidget

class SNBTManager(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.current_widget = None
        self.current_name = None

        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True, padx=5, pady=5)

        self.available_snbts = {
            "attack_range": AttackRangeWidget,
            "attribute_modifier": AttributeModifierWidget,
            "banner_patterns": BannerPatternsWidget,
            "base_color": BaseColorWidget,
            "bees": BeesWidget,
            "block_entity_data": BlockEntityDataWidget,
            "block_state": BlockStateWidget,
            "blocks_attacks": BlocksAttacksWidget,
            "break_sound": BreakSoundWidget,
            "bucket_entity_data": BucketEntityDataWidget,
            "bundle_contents": BundleContentsWidget,
            "can_break": CanBreakWidget,
            "can_place_on": CanPlaceOnWidget,
            "charged_projectiles": ChargedProjectilesWidget,
            "consumable": ConsumableWidget,
            "container": ContainerWidget,
            "container_loot": ContainerLootWidget,
            "custom_data": CustomDataWidget,
            "custom_name": CustomNameWidget,
            "damage": DamageWidget,
            "damage_resistant": DamageResistantWidget,
            "damage_type": DamageTypeWidget,
            "death_protection": DeathProtectionWidget,
            "dye": DyeWidget,
            "dyed_color": DyedColorWidget,
            "enchantable": EnchantableWidget,
            "enchantment_glint_override": EnchantmentGlintOverrideWidget,
            "enchantments": EnchantmentsWidget,
            "entity_data": EntityDataWidget,
            "equippable": EquippableWidget,
            "firework_explosion": FireworkExplosionWidget,
            "fireworks": FireworksWidget,
            "food": FoodWidget,
            "glider": GliderWidget,
            "instrument": InstrumentWidget,
            "intangible_projectile": IntangibleProjectileWidget,
            "item_model": ItemModelWidget,
            "item_name": ItemNameWidget,
            "jukebox_playable": JukeboxPlayableWidget,
            "kinetic_weapon": KineticWeaponWidget,
            "lock": LockWidget,
            "lodestone_tracker": LodestoneTrackerWidget,
            "lore": LoreWidget,
            "map_color": MapColorWidget,
            "map_id": MapIdWidget,
            "max_damage": MaxDamageWidget,
            "max_stack_size": MaxStackSizeWidget,
            "minimum_attack_charge": MinimumAttackChargeWidget,
            "note_block_sound": NoteBlockSoundWidget,
            "ominous_bottle_amplifier": OminousBottleAmplifierWidget,
            "piercing_weapon": PiercingWeaponWidget,
            "pot_decorations": PotDecorationsWidget,
            "potion_contents": PotionContentsWidget,
            "potion_duration_scale": PotionDurationScaleWidget,
            "profile": ProfileWidget,
            "provides_banner_patterns": ProvidesBannerPatternsWidget,
            "rarity": RarityWidget,
            "recipes": RecipesWidget,
            "repair_cost": RepairCostWidget,
            "repairable": RepairableWidget,
            "stored_enchantments": StoredEnchantmentsWidget,
            "suspicious_stew_effects": SuspiciousStewEffectsWidget,
            "tool": ToolWidget,
            "tooltip_display": TooltipDisplayWidget,
            "unbreakable": UnbreakableWidget,
            "use_cooldown": UseCooldownWidget,
            "use_effects": UseEffectsWidget,
            "use_remainder": UseRemainderWidget,
            "weapon": WeaponWidget,
            "writable_book_content": WritableBookContentWidget
        }

        self.added_components = {}

        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', pady=(0, 5))

        tk.Label(top_frame, text=bc.get_lang_text("dropdown.selectsnbt")).pack(side='left')
        self.combo = ttk.Combobox(top_frame, values=list(self.available_snbts.keys()),
                                  state='readonly', width=20)
        self.combo.pack(side='left', padx=5)
        if self.available_snbts:
            self.combo.current(0)

        self.add_btn = ttk.Button(top_frame, text=bc.get_lang_text("button.addsnbt"),
                                  command=self._add_current)
        self.add_btn.pack(side='left')

        mid_frame = tk.Frame(self)
        mid_frame.pack(fill='both', expand=True, pady=5)
        tk.Label(mid_frame, text=bc.get_lang_text("textbox.addedsnbt")).pack(anchor='w')
        self.listbox = tk.Listbox(mid_frame, height=4)
        self.listbox.pack(fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

        self.config_frame = tk.Frame(self, relief='sunken', bd=1, height=300)
        self.config_frame.pack(fill='x', pady=5)
        self.config_frame.pack_propagate(False)
        self.placeholder_label = tk.Label(self.config_frame, text="Select a component to edit")
        self.placeholder_label.pack(fill='both', expand=True)

    def _add_current(self):
        name = self.combo.get()
        if not name:
            return
        if name in self.added_components:
            messagebox.showerror(bc.get_lang_text("msgbox.error.duplicated"),
                                 bc.get_lang_text("msgbox.error.duplicated_format").format(name=name))
            return
        widget_class = self.available_snbts[name]
        widget = widget_class(self.config_frame)
        widget.pack(fill='both', expand=True)
        widget.pack_forget()
        self.added_components[name] = widget
        self.listbox.insert(tk.END, name)
        messagebox.showinfo(bc.get_lang_text("msgbox.info.addedsnbt"),
                            bc.get_lang_text("msgbox.info.addedsnbt_format").format(name=name))

    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        if name == self.current_name:
            return
        if self.current_widget:
            self.current_widget.pack_forget()
        self.current_widget = self.added_components[name]
        self.current_widget.pack(fill='both', expand=True)
        self.current_name = name

    def get_combined_snbt(self):
        parts = []
        for widget in self.added_components.values():
            nbt = widget.get_nbt()
            if nbt:
                parts.append(nbt)
        return ','.join(parts)

def create_snbt_manager(parent):
    return SNBTManager(parent)

create_snbt_selector = create_snbt_manager