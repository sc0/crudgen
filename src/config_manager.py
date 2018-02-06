import yaml
import os
from src.yaml_object import YamlObject


class ConfigManager:

    class Configuration:

        def __init__(self, data):
            self.path = data['path']
            self.output = data['output']
            self.files = data['files']

    def __init__(self):
        config_file = open('config/config.yml', 'r')
        self.config = ConfigManager.Configuration(yaml.load(config_file))
        config_file.close()
        self.yaml_data = None

    def load_input(self, file):
        yaml_file = open(file, 'r')
        self.yaml_data = yaml.load(yaml_file)
        yaml_file.close()

        return YamlObject(self.yaml_data)

    def generate_files(self):
        pass
