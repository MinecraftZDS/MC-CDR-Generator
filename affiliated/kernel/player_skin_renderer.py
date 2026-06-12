from PIL import Image, ImageTk
import requests
from io import BytesIO

def fetch_skin_image(skin_url):
    try:
        resp = requests.get(skin_url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        return img
    except Exception as e:
        print(f"[skin_renderer] Failed to fetch skin: {e}")
        return None

def render_avatar(skin_img, scale=8, layer2_scale=1.2):
    if skin_img is None:
        return None
    if skin_img.mode != 'RGBA':
        skin_img = skin_img.convert('RGBA')

    layer1 = skin_img.crop((8, 8, 16, 16))
    base_size = 8 * scale
    img_layer1 = layer1.resize((base_size, base_size), Image.NEAREST)

    try:
        layer2 = skin_img.crop((40, 8, 48, 16))
        layer2_resized = layer2.resize((base_size, base_size), Image.NEAREST)
        new_w = int(base_size * layer2_scale)
        new_h = int(base_size * layer2_scale)
        layer2_scaled = layer2_resized.resize((new_w, new_h), Image.NEAREST)

        final_w = max(base_size, new_w)
        final_h = max(base_size, new_h)
        final_img = Image.new('RGBA', (final_w, final_h), (0, 0, 0, 0))

        x1 = (final_w - base_size) // 2
        y1 = (final_h - base_size) // 2
        final_img.paste(img_layer1, (x1, y1), img_layer1)

        x2 = (final_w - new_w) // 2
        y2 = (final_h - new_h) // 2
        final_img.paste(layer2_scaled, (x2, y2), layer2_scaled)

        return final_img
    except:
        return img_layer1

def skin_to_tk(skin_url, scale=8, layer2_scale=1.1):
    img = fetch_skin_image(skin_url)
    if img is None:
        return None
    avatar = render_avatar(img, scale, layer2_scale)
    return ImageTk.PhotoImage(avatar) if avatar else None