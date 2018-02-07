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
            self.output_names = data['output_names']

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
        class_name_regex = re.compile('{{\s?class_name\s?}}')
        lclass_name_regex = re.compile('{{\s?_class_name\s?}}')
        plural_class_name_regex = re.compile('{{\s?class_name_plural\s?}}')
        plural_lclass_name_regex = re.compile('{{\s?_class_name_plural\s?}}')
        foreach_field_regex = re.compile('{{\s?foreach_field\s?}}')
        end_regex = re.compile('{{\s?end\s?}}')
        field_regex = re.compile('{{\s?field\s?}}')
        type_regex = re.compile('{{\s?type\s?}}')

        for filename in self.config.files:
            def lower_first(s): return s[:1].lower() + s[1:] if s else ''

            with open(os.path.join('templates', filename), 'r') as input_file:
                with open(os.path.join(self.config.output, filename), 'w') as output_file:
                    while True:
                        line = input_file.readline()
                        if line == '':
                            break

                        line = class_name_regex.subn(self.yaml_object.class_name.capitalize(), line)[0]
                        line = lclass_name_regex.subn(lower_first(self.yaml_object.class_name), line)[0]
                        line = plural_class_name_regex.subn(self.yaml_object.plural_class_name.capitalize(), line)[0]
                        line = plural_lclass_name_regex.subn(lower_first(self.yaml_object.plural_class_name), line)[0]

                        if foreach_field_regex.search(line) is not None:
                            field_lines = []

                            while end_regex.search(line) is None:
                                line = input_file.readline()
                                if line == '':
                                    raise Exception('Expected {{end}}, EOF reached instead')
                                field_lines.append(line)

                            for field in self.yaml_object.fields:
                                for line in field_lines:
                                    if end_regex.search(line) is not None:
                                        line = ''
                                        break
                                    line = class_name_regex.subn(self.yaml_object.class_name.capitalize(), line)[0]
                                    line = lclass_name_regex.subn(lower_first(self.yaml_object.class_name), line)[0]
                                    line = plural_class_name_regex.subn(self.yaml_object.plural_class_name.capitalize(), line)[0]
                                    line = plural_lclass_name_regex.subn(lower_first(self.yaml_object.plural_class_name), line)[0]
                                    line = field_regex.subn(field.name, line)[0]
                                    line = type_regex.subn(field.type, line)[0]
                                    output_file.write(line)

                        output_file.write(line)

        for index in range(0, len(self.config.files)):
            filename = class_name_regex.subn(self.yaml_object.class_name.capitalize(), self.config.output_names[index])[0]
            os.rename(os.path.join('output', self.config.files[index]), os.path.join('output', filename))



