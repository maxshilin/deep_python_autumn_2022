import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_single_element_usecase(self):
        cache = LRUCache(1)

        cache["key1"] = "value1"
        self.assertEqual(cache["key1"], "value1")
        self.assertEqual(cache["key2"], None)

        cache["key2"] = "value2"
        self.assertEqual(cache["key1"], None)
        self.assertEqual(cache["key2"], "value2")

        cache["key2"] = "value3"
        self.assertEqual(cache["key2"], "value3")

    def test_some_elements_usecase(self):
        cache = LRUCache(2)

        cache["key1"] = "value1"
        cache["key2"] = "value2"

        self.assertEqual(cache["key3"], None)
        self.assertEqual(cache["key2"], "value2")
        self.assertEqual(cache["key1"], "value1")

        cache["key3"] = "value3"

        self.assertEqual(cache["key3"], "value3")
        self.assertEqual(cache["key2"], None)
        self.assertEqual(cache["key1"], "value1")

    def test_update_priority_by_reassignment(self):
        cache = LRUCache(2)

        cache["key1"] = "value1"
        cache["key2"] = "value2"

        cache["key1"] = "new_value1"
        cache["key3"] = "value3"

        self.assertEqual(cache["key1"], "new_value1")
        self.assertEqual(cache["key2"], None)
        self.assertEqual(cache["key3"], "value3")

        cache = LRUCache(3)

        cache["key1"] = "value1"
        cache["key2"] = "value2"
        cache["key3"] = "value3"

        cache["key2"] = "new_value2"
        self.assertEqual(cache["key1"], "value1")
        cache["key4"] = "value4"

        self.assertEqual(cache["key1"], "value1")
        self.assertEqual(cache["key2"], "new_value2")
        self.assertEqual(cache["key3"], None)
        self.assertEqual(cache["key4"], "value4")

    def test_update_priority_by_request(self):
        cache = LRUCache(2)

        cache["key1"] = "value1"
        cache["key2"] = "value2"

        self.assertEqual(cache["key1"], "value1")
        cache["key3"] = "value3"

        self.assertEqual(cache["key1"], "value1")
        self.assertEqual(cache["key2"], None)
        self.assertEqual(cache["key3"], "value3")

    def test_get_method(self):
        cache = LRUCache(2)

        cache["key1"] = "value1"
        cache["key2"] = "value2"

        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")

        self.assertIsNone(cache.get("key3"))
        self.assertEqual(cache.get("key3", "value3"), "value3")

    def test_update_priority_by_get(self):
        cache = LRUCache(2)

        cache["key1"] = "value1"
        cache["key2"] = "value2"

        self.assertEqual(cache.get("key1"), "value1")
        cache["key3"] = "value3"

        self.assertEqual(cache["key1"], "value1")
        self.assertEqual(cache["key2"], None)
        self.assertEqual(cache["key3"], "value3")


if __name__ == "__main__":
    unittest.main()
