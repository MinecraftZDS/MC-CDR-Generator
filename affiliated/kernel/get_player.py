import requests
import json
import sys

def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('id'), data.get('name')
        else:
            return None, None
    except Exception as e:
        print(f"[get_player] Error: {e}", file=sys.stderr)
        return None, None

def get_skin_url(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            properties = data.get('properties', [])
            for prop in properties:
                if prop.get('name') == 'textures':
                    import base64
                    decoded = base64.b64decode(prop.get('value')).decode('utf-8')
                    textures = json.loads(decoded)
                    skin_url = textures.get('textures', {}).get('SKIN', {}).get('url')
                    return skin_url
        return None
    except Exception as e:
        print(f"[get_player] Error: {e}", file=sys.stderr)
        return None