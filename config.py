import json

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)
