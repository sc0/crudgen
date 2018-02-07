import yaml
import os
import re
from src.yaml_object import YamlObject


class ConfigManager:

    class Configuration:

        def __init__(self, data):
            self.path = data['path']
            self.output = data['output']
            self.files = data['files']

    def __init__(self):
        with open('config/config.yml', 'r') as config_file:
            self.config = ConfigManager.Configuration(yaml.load(config_file))

        self.yaml_data = None
        self.yaml_object = None

    def load_input(self, file):
        with open(file, 'r') as yaml_file:
            self.yaml_data = yaml.load(yaml_file)

        self.yaml_object = YamlObject(self.yaml_data)
        return self.yaml_object

    def generate_files(self):
        for filename in self.config.files:
            class_name_regex = re.compile('{{\s?class_name\s?}}')
            lclass_name_regex = re.compile('{{\s?_class_name\s?}}')

            lower_first = lambda s: s[:1].lower() + s[1:] if s else ''

            with open(os.path.join('templates', filename), 'r') as input_file:
                with open(os.path.join(self.config.output, filename), 'w') as output_file:
                    while True:
                        line = input_file.readline()
                        if line == '':
                            break
                        line = class_name_regex.subn(self.yaml_object.class_name.capitalize(), line)[0]
                        line = lclass_name_regex.subn(lower_first(self.yaml_object.class_name), line)[0]
                        output_file.write(line)



