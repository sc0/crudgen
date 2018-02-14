import yaml
import os
import re
from src.yaml_object import YamlObject


class ConfigManager:

    class Configuration:

        def __init__(self, data):
            self.output = data['output']
            self.templates_dir = data['templates']
            self.files = data['files']
            self.output_names = data['output_names']
            self.output_dirs = data['output_directories']

    def __init__(self, config_file, output_root):
        with open(config_file, 'r') as config_file:
            self.config = ConfigManager.Configuration(yaml.load(config_file))

        self.yaml_data = None
        self.yaml_object = None
        self.output_root = output_root

    def load_input(self, file):
        with open(file, 'r') as yaml_file:
            self.yaml_data = yaml.load(yaml_file)

        self.yaml_object = YamlObject(self.yaml_data)
        return self.yaml_object

    def generate_files(self):
        def lower_first(s): return s[:1].lower() + s[1:] if s else ''

        def upper_first(s): return s[:1].upper() + s[1:] if s else ''

        class_name_regex = re.compile('{{\s?class_name\s?}}')
        lclass_name_regex = re.compile('{{\s?_class_name\s?}}')
        plural_class_name_regex = re.compile('{{\s?class_name_plural\s?}}')
        plural_lclass_name_regex = re.compile('{{\s?_class_name_plural\s?}}')
        foreach_field_regex = re.compile('{{\s?foreach_field\s?}}')
        end_regex = re.compile('{{\s?end\s?}}')
        field_regex = re.compile('{{\s?field\s?}}')
        type_regex = re.compile('{{\s?type\s?}}')
        uppercase_type_regex = re.compile('{{\s?\^\s?type\s?}}')
        output_path = os.path.join(self.config.output, self.output_root)

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        for final_dir in self.config.output_dirs:
            if not os.path.exists(os.path.join(output_path, final_dir)):
                os.mkdir(os.path.join(output_path, final_dir))

        for filename in self.config.files:

            with open(os.path.join(self.config.templates_dir, filename), 'r') as input_file:
                with open(os.path.join(output_path, filename), 'w') as output_file:
                    while True:
                        line = input_file.readline()
                        if line == '':
                            break

                        line = class_name_regex.subn(upper_first(self.yaml_object.class_name), line)[0]
                        line = lclass_name_regex.subn(lower_first(self.yaml_object.class_name), line)[0]
                        line = plural_class_name_regex.subn(upper_first(self.yaml_object.plural_class_name), line)[0]
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
                                    line = class_name_regex.subn(upper_first(self.yaml_object.class_name), line)[0]
                                    line = lclass_name_regex.subn(lower_first(self.yaml_object.class_name), line)[0]
                                    line = plural_class_name_regex.subn(upper_first(self.yaml_object.plural_class_name), line)[0]
                                    line = plural_lclass_name_regex.subn(lower_first(self.yaml_object.plural_class_name), line)[0]
                                    line = field_regex.subn(field.name, line)[0]
                                    line = type_regex.subn(field.type, line)[0]
                                    line = uppercase_type_regex.subn(upper_first(field.type), line)[0]
                                    output_file.write(line)

                        output_file.write(line)

        for index in range(0, len(self.config.files)):
            filename = class_name_regex.subn(upper_first(self.yaml_object.class_name), self.config.output_names[index])[0]
            os.rename(os.path.join(output_path, self.config.files[index]), os.path.join(output_path, self.config.output_dirs[index], filename))



