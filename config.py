# config.py

import json


def load_config(config_file='config.json', logger=None):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        message = f"Config file '{config_file}' not found. Please create it before running the game."
        if logger:
            logger.error(message)
        else:
            print(message)
        raise SystemExit(1)
    except json.JSONDecodeError:
        message = f"Error parsing JSON from '{config_file}'. Please ensure it is correctly formatted."
        if logger:
            logger.error(message)
        else:
            print(message)
        raise SystemExit(1)
