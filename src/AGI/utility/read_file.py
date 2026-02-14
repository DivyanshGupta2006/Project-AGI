from AGI.utility import get_path, get_config


config = get_config.load()

def read_prompt():
    with open(get_path.absolute(config['paths']['prompt']), "r", encoding="utf-8") as f:
        content = f.read().strip()
    return content