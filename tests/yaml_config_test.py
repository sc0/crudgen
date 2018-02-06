import unittest
from src.config_manager import ConfigManager
from src.yaml_object import YamlObject


class TestYamlTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestYamlTests, self).__init__(*args, **kwargs)

        self.cfg = ConfigManager()

    def test_load_config(self):
        self.assertTrue('map' in self.cfg.config)
        self.assertTrue('interface' in self.cfg.config['map'])
        self.assertEqual(len(self.cfg.config['map']), 4)

    def test_load_yaml_object(self):
        obj = self.cfg.load_input('input/person.yml')

        self.assertIsInstance(obj, YamlObject)
        self.assertEqual(obj.class_name, 'person')
        self.assertEqual(len(obj.fields), 3)
        self.assertIsInstance(obj.fields[0], YamlObject.Field)
        self.assertEqual(obj.fields[0].name, 'name')


