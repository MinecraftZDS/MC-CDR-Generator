import tkinter as tk
from tkinter import ttk
import threading
from affiliated.kernel.get_player import get_uuid, get_skin_url
from affiliated.kernel.player_skin_renderer import skin_to_tk

class PlayerSkinViewer(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)

        self.avatar_image = None

        self.status_label = tk.Label(self, text="", font=('Arial', 10))
        self.status_label.pack(pady=2)

        self.canvas = tk.Canvas(self, width=128, height=128, bg='gray')
        self.canvas.pack(pady=10)
        self.canvas_image = None

        self.current_name = None

    def query_and_display(self, player_name):
        if not player_name:
            self._set_status("Player name cannot be empty", "red")
            return
        self._set_status("Fetching...", "green")
        thread = threading.Thread(target=self._do_fetch, args=(player_name,), daemon=True)
        thread.start()

    def _do_fetch(self, name):
        print(f"[PlayerSkinViewer] Fetching UUID for {name}")
        uuid, exact_name = get_uuid(name)
        if not uuid:
            self._update_status("Player not found", "red")
            print("[PlayerSkinViewer] UUID not found")
            return
        print(f"[PlayerSkinViewer] UUID: {uuid}")

        skin_url = get_skin_url(uuid)
        if not skin_url:
            self._update_status("Skin not found", "red")
            print("[PlayerSkinViewer] Skin URL not found")
            return
        print(f"[PlayerSkinViewer] Skin URL: {skin_url}")

        try:
            photo = skin_to_tk(skin_url, scale=8)
            if photo:
                self._update_avatar(photo)
                self._update_status(f"Found: {exact_name}", "green")
                print("[PlayerSkinViewer] Avatar rendered successfully")
            else:
                self._update_status("Failed to render skin", "red")
                print("[PlayerSkinViewer] Rendering failed")
        except Exception as e:
            print(f"[PlayerSkinViewer] Error: {e}")
            self._update_status("Error loading skin", "red")

    def _update_status(self, text, color):
        self.status_label.after(0, lambda: self.status_label.config(text=text, fg=color))

    def _set_status(self, text, color):
        self.status_label.after(0, lambda: self.status_label.config(text=text, fg=color))

    def _update_avatar(self, photo):
        self.avatar_image = photo
        self.canvas.after(0, lambda: self._draw_avatar())

    def _draw_avatar(self):
        self.canvas.delete("all")
        self.canvas.create_image(64, 64, image=self.avatar_image, anchor='center')
        self.canvas_image = self.avatar_image