from src.config_manager import ConfigManager

if __name__ == "__main__":
    cfg = ConfigManager()
    obj = cfg.load_input('input/person.yml')
