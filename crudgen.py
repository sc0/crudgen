import argparse
from src.config_manager import ConfigManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_root', type=str)

    args = parser.parse_args()

    cfg = ConfigManager(args.output_root)
    obj = cfg.load_input(args.input_file)
    cfg.generate_files()
