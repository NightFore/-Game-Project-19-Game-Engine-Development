import json
import logging

logger = logging.getLogger(__name__)


def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Config file '{config_file}' not found. Please create it before running the game.")
        raise SystemExit(1)
    except json.JSONDecodeError:
        logger.error(f"Error parsing JSON from '{config_file}'. Please ensure it is correctly formatted.")
        raise SystemExit(1)
