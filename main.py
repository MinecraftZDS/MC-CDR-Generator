import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import affiliated.kernel.basic_components as bc
import affiliated.kernel.command_return as cmd_ui
import affiliated.kernel.select_snbt as snbt_selector
from affiliated.kernel.select_nbt import EntityNBTSelector
from affiliated.kernel.coordinate_dialog import CoordinateDialog

def main():
    saved_lang = bc.load_config()
    bc.load_language(saved_lang)

    root = tk.Tk()
    root.title(bc.get_lang_text("window.title"))
    root.geometry("950x800")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 语言菜单
    lang_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=bc.get_lang_text("menu.root.language"), menu=lang_menu)
    languages = [
        ("简体中文", "zh_cn"),
        ("繁體中文（台灣）", "zh_tw"),
        ("繁體中文（香港）", "zh_hk"),
        ("English (US)", "en_us"),
        ("English (GB)", "en_gb"),
        ("日本語", "ja_jp"),
        ("한국어", "ko_kr"),
        ("Русский", "ru_ru"),
        ("猫猫语", "lol_cn"),
        ("文言", "lzh")
    ]
    def change_language(lang_code):
        bc.load_language(lang_code)
        messagebox.showinfo(
            bc.get_lang_text("msgbox.title.restart_required"),
            bc.get_lang_text("msgbox.info.restart_required")
        )
    for display_name, lang_code in languages:
        lang_menu.add_command(label=display_name, command=lambda lc=lang_code: change_language(lc))

    # Wiki 菜单
    wiki_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=bc.get_lang_text("menu.root.wiki"), menu=wiki_menu)
    def open_wiki(page):
        webbrowser.open(f"https://zh.minecraft.wiki/w/{page}")
    wiki_menu.add_command(label=bc.get_lang_text("menu.sub.snbt"), command=lambda: open_wiki("数据组件"))
    wiki_menu.add_command(label=bc.get_lang_text("menu.sub.nbt"), command=lambda: open_wiki("实体数据格式"))
    wiki_menu.add_command(label=bc.get_lang_text("menu.sub.text"), command=lambda: open_wiki("文本组件"))

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=5, pady=5)

    give_frame = ttk.Frame(notebook)
    notebook.add(give_frame, text=bc.get_lang_text("notebook.give"))
    tk.Label(give_frame, text=bc.get_lang_text("inputbox.gaveitem")).pack(anchor='w', padx=5, pady=(10, 0))
    give_entry = tk.Entry(give_frame, width=50)
    give_entry.pack(fill='x', padx=5, pady=(0, 10))
    snbt_mgr = snbt_selector.create_snbt_manager(give_frame)

    summon_frame = ttk.Frame(notebook)
    notebook.add(summon_frame, text=bc.get_lang_text("notebook.summon"))

    top_frame = tk.Frame(summon_frame)
    top_frame.pack(fill='x', padx=5, pady=(10, 0))
    tk.Label(top_frame, text=bc.get_lang_text("inputbox.summonedentity")).pack(side='left')
    summon_entry = tk.Entry(top_frame, width=30)
    summon_entry.pack(side='left', fill='x', expand=True, padx=5)

    summon_coord = ""
    def edit_coord():
        nonlocal summon_coord
        dialog = CoordinateDialog(root, summon_coord)
        new_coord = dialog.show()
        if new_coord is not None:
            summon_coord = new_coord
            coord_label.config(text=bc.get_lang_text("coordinate.set") + f" {summon_coord}" if summon_coord else "")
    coord_btn = ttk.Button(top_frame, text=bc.get_lang_text("coordinate.edit_btn"), command=edit_coord)
    coord_btn.pack(side='left', padx=5)
    coord_label = tk.Label(summon_frame, text="", fg="blue")
    coord_label.pack(anchor='w', padx=5, pady=(0, 5))

    entity_nbt_mgr = EntityNBTSelector(summon_frame)

    preview_text, generate_btn, copy_btn = cmd_ui.add_command_controls(root)

    def on_generate():
        current_tab = notebook.select()
        tab_text = notebook.tab(current_tab, "text")
        if tab_text == bc.get_lang_text("notebook.give"):
            item_name = give_entry.get().strip()
            if not item_name:
                messagebox.showwarning(bc.get_lang_text("msgbox.warning.emptyitem"), "Item name cannot be empty!")
                return
            combined_nbt = snbt_mgr.get_combined_snbt()
            if combined_nbt:
                cmd = f"/give @p {item_name}[{combined_nbt}]"
            else:
                cmd = f"/give @p {item_name}"
        else:  # summon
            entity_name = summon_entry.get().strip()
            if not entity_name:
                cmd = ""
            elif entity_name == "player" or entity_name == "minecraft:player":
                messagebox.showerror(bc.get_lang_text("error.title"),
                                     bc.get_lang_text("msgbox.error.cannot_summon_player"))
                return
            else:
                entity_nbt = entity_nbt_mgr.get_combined_nbt()
                if summon_coord:
                    if entity_nbt:
                        cmd = f"/summon {entity_name} {summon_coord} {entity_nbt}"
                    else:
                        cmd = f"/summon {entity_name} {summon_coord}"
                else:
                    if entity_nbt:
                        cmd = f"/summon {entity_name} ~ ~ ~ {entity_nbt}"
                    else:
                        cmd = f"/summon {entity_name}"
        preview_text.config(state='normal')
        preview_text.delete(1.0, tk.END)
        preview_text.insert(tk.END, cmd)
        preview_text.config(state='disabled')

    generate_btn.config(command=on_generate)
    give_entry.bind("<Return>", lambda e: on_generate())
    summon_entry.bind("<Return>", lambda e: on_generate())

    def on_copy():
        cmd = preview_text.get(1.0, tk.END).strip()
        if cmd and not cmd.startswith("#"):
            root.clipboard_clear()
            root.clipboard_append(cmd)
    copy_btn.config(command=on_copy)

    root.mainloop()

if __name__ == "__main__":
    main()