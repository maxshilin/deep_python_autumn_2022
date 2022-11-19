import logging
import sys


class LRUCache(dict):
    def __init__(self, limit=42):
        self.limit = limit
        super().__init__()

        self.logger = logging.getLogger("lru_cache")
        self.logger.debug("cache object created")

    def __getitem__(self, key):
        self.logger.info("key: %s has been requested", key)
        if not super().__contains__(key):
            self.logger.warning("key: %s does not exist in cache", key)
            return None

        value = super().pop(key)
        super().__setitem__(key, value)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.logger.info("value: %s has been assigned to key: %s", key, value)

        if super().__contains__(key):
            super().pop(key)
            super().__setitem__(key, value)
            self.logger.warning(
                "value: %s has been reassigned by value %s",
                super().__getitem__(key),
                value,
            )
            return None

        if len(self) >= self.limit:
            low_priority_key = list(super().keys())[0]
            self.logger.info(
                "item %s:%s has been removed from cache",
                low_priority_key,
                super().__getitem__(low_priority_key),
            )
            super().pop(low_priority_key)

        super().__setitem__(key, value)
        return None

    def get(self, key, value=None):
        out = self[key]

        if out:
            return out
        return value


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s\t%(levelname)s\t%(message)s",
        filename="lru_cache.log",
    )
    lru = logging.getLogger("lru_cache")

    if len(sys.argv) > 1 and "-s" in sys.argv:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s -"
            " %(message)s"
        )
        handler.setFormatter(formatter)
        lru.addHandler(handler)

    cache = LRUCache(2)

    # pylint: disable=pointless-statement
    cache["key1"] = "value1"
    cache["key1"]
    cache["key2"] = "value2"
    cache["key2"]
    cache["key3"] = "value3"
    cache["key3"]
    cache["key1"]
