import json

from AGI.utility import get_path, get_config

config = get_config.load()
path = get_path.absolute(config['paths']['state'])

def update(idx):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"api_index": idx}, f)