import json

DEFAULT_CACHE_FILE_NAME = "cache.json"

class StringCache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4, sort_keys=True)

    def get(self, key):
        return self.cache.get(key, None)

    def set(self, key, value):
        self.cache[key] = value

if __name__ == '__main__':
    cache = StringCache('cache.json')
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.save_cache()