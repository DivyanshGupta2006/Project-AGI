import os
import time
import heapq
from dotenv import load_dotenv

from AGI.utility import read_file, update_state


class APIKey:
    def __init__(self, key_string, tokens_left=4000000, reset_time=0.0):
        self.key = key_string
        self.tokens_left = tokens_left
        self.reset_time = reset_time

    def __lt__(self, other):
        if self.reset_time == other.reset_time:
            return self.tokens_left > other.tokens_left
        return self.reset_time < other.reset_time


class KeyManager:
    def __init__(self):
        load_dotenv()
        raw_keys = [v for k, v in os.environ.items() if k.startswith("API_KEY") and v]

        if not raw_keys:
            raise ValueError("No keys found in .env")

        try:
            state = read_file.read_state()
        except Exception:
            state = {}

        self.key_heap = []

        for k in raw_keys:
            key_state = state.get(k, {})
            api_key = APIKey(
                key_string=k,
                tokens_left=key_state.get("tokens_left", 4000000),
                reset_time=key_state.get("reset_time", 0.0)
            )
            heapq.heappush(self.key_heap, api_key)

    def get_key(self) -> APIKey:
        if not self.key_heap:
            raise ValueError("No keys available in the pool.")

        best_key = self.key_heap[0]

        current_time = time.time()
        if best_key.reset_time > current_time:
            wait_time = best_key.reset_time - current_time
            print(f"Rate limit hit across all keys. Sleeping for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

        return heapq.heappop(self.key_heap)

    def report_usage(self, api_key: APIKey, tokens_used: int = 0, rate_limited: bool = False,
                     reset_in_seconds: int = 60):
        if rate_limited:
            api_key.reset_time = time.time() + reset_in_seconds
        else:
            api_key.tokens_left -= tokens_used
            api_key.tokens_left = max(0, api_key.tokens_left)

        heapq.heappush(self.key_heap, api_key)
        self._save_state()

    def _save_state(self):
        state = {}
        for k in self.key_heap:
            state[k.key] = {
                "tokens_left": k.tokens_left,
                "reset_time": k.reset_time
            }
        update_state.update(state)