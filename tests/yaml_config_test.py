import unittest
from src.config_manager import ConfigManager
from src.yaml_object import YamlObject


class TestYamlTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestYamlTests, self).__init__(*args, **kwargs)

        self.cfg = ConfigManager()

    def test_load_config(self):
        self.assertEqual(self.cfg.config.path, 'input/person.yml')
        self.assertEqual(self.cfg.config.output, 'output')
        self.assertEqual(len(self.cfg.config.files), 4, self.cfg.config.files)

    def test_load_yaml_object(self):
        obj = self.cfg.load_input('input/person.yml')

        self.assertIsInstance(obj, YamlObject)
        self.assertEqual(obj.class_name, 'person')
        self.assertEqual(len(obj.fields), 3)
        self.assertIsInstance(obj.fields[0], YamlObject.Field)
        self.assertEqual(obj.fields[0].name, 'name')
        self.assertEqual(obj.plural_class_name, 'persons')


