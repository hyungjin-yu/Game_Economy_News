import json
import os

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            # If config file missing, return empty dict to rely on env vars
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def get(self, key, default=None):
        # 1. Check Environment Variable (Upper case standard)
        env_val = os.environ.get(key.upper())
        if env_val:
            return env_val
            
        # 2. Check Config File
        return self.config.get(key, default)
