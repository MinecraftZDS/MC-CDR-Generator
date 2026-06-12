import json
import os

# 全局变量
_current_lang = "en_us"
_lang_data = {}

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('language', 'en_us')
    except:
        return 'en_us'

def save_config(lang_code):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({'language': lang_code}, f, indent=2)
    except Exception as e:
        print(f"Failed to save config: {e}")

def load_language(lang_code):
    global _current_lang, _lang_data
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    lang_path = os.path.join(base_dir, 'lang', f'{lang_code}.json')
    try:
        with open(lang_path, 'r', encoding='utf-8') as f:
            _lang_data = json.load(f)
        _current_lang = lang_code
        save_config(lang_code)
    except Exception as e:
        print(f"Warning: Cannot load {lang_code}.json, using empty data. {e}")
        _lang_data = {}
        _current_lang = lang_code

def get_lang_text(key):
    return _lang_data.get(key, key)

def get_current_lang():
    return _current_lang