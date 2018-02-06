import yaml

from src.yaml_object import YamlObject


class ConfigManager:

    def __init__(self):
        config_file = open('config/config.yml', 'r')
        self.config = yaml.load(config_file)
        config_file.close()
        self.yaml_data = None

    def load_input(self, file):
        yaml_file = open(file, 'r')
        self.yaml_data = yaml.load(yaml_file)
        yaml_file.close()

        return YamlObject(self.yaml_data)

