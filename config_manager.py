import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_key": "",
    "target_language": "English",
    "hotkey": "ctrl+shift+x"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving config: {e}")

def get_api_key():
    config = load_config()
    return config.get("api_key", "")

def get_target_language():
    config = load_config()
    return config.get("target_language", "English")

def get_hotkey():
    config = load_config()
    return config.get("hotkey", "ctrl+shift+x")
