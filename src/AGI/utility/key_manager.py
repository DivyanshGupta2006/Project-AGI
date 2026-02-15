import os

from dotenv import load_dotenv

from AGI.utility import read_file, update_state


class Key:
    def __init__(self):
        load_dotenv()
        self.keys = [v for k, v in os.environ.items() if k.startswith("API_KEY") and v]

        try:
            state = read_file.read_state()
            self.idx = state["api_index"]
        except:
            self.idx = 0

    def get_key(self):
        if not self.keys: raise ValueError("No keys found in .env")
        key = self.keys[self.idx % len(self.keys)]
        self.rotate()
        return key

    def rotate(self):
        self.idx = (self.idx + 1) % len(self.keys)
        update_state.update(self.idx)