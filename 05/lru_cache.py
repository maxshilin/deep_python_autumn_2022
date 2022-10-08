class LRUCache(dict):
    def __init__(self, limit=42):
        self.limit = limit

        super().__init__()

    def __getitem__(self, key):
        if not super().__contains__(key):
            return None

        value = super().pop(key)
        super().__setitem__(key, value)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if super().__contains__(key):
            super().pop(key)
            super().__setitem__(key, value)
            return None

        if len(self) >= self.limit:
            super().pop(list(super().keys())[0])

        super().__setitem__(key, value)
        return None

    def get(self, key, value=None):
        out = self[key]

        if out:
            return out
        return value
