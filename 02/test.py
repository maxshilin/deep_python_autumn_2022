from unittest.mock import patch
import unittest
from faker import Faker

from parse_json import parse_json


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()

        self.first_names = [self.fake.first_name() for _ in range(3)]
        self.last_names = [self.fake.last_name() for _ in range(3)]
        self.phone_number = [self.fake.phone_number() for _ in range(1, 6)]
        self.random_ints = [
            str(self.fake.random_int(20, 80)) for _ in range(3)
        ]

        self.json = [
            {
                "json_str": {
                    "firstName": self.first_names,
                    "lastName": self.last_names,
                    "phoneNumber": self.phone_number,
                    "number": self.random_ints,
                }
            }
        ]

    @patch("parse_json.keyword_callback")
    def test_empty_inputs(self, mock_keyword_callback):
        json_str = '{"key1": "123 34 123", "key2": "value 123", "key3": null}'
        required_fields = ["key1", "key2"]
        keywords = ["123", "value"]

        self.assertIsNone(parse_json("", mock_keyword_callback, [], []))
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(parse_json(json_str, mock_keyword_callback, [], []))
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(
            parse_json("", mock_keyword_callback, required_fields, [])
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(parse_json("", mock_keyword_callback, [], keywords))
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(
            parse_json(json_str, mock_keyword_callback, required_fields, [])
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(
            parse_json(json_str, mock_keyword_callback, [], keywords)
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertIsNone(
            parse_json("", mock_keyword_callback, required_fields, keywords)
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @patch("parse_json.keyword_callback")
    def test_manual_json(self, mock_keyword_callback):
        json_str = '{"key1": "123 34 123", "key2": "value 123", "key3": null}'
        required_fields = ["key1", "key2"]
        keywords = ["123", "value"]
        self.assertDictEqual(
            parse_json(
                json_str, mock_keyword_callback, required_fields, keywords
            ),
            {"123": 3, "value": 1},
        )
        self.assertEqual(mock_keyword_callback.call_count, 4)

    @patch("json.loads")
    @patch("parse_json.keyword_callback")
    def test_faker_json(self, mock_keyword_callback, mock_json_loads):
        json_str = " "
        required_fields = ["key1", "key2"]
        keywords = ["123", "value"]

        mock_json_loads.return_value = {
            "key1": "123 34 123",
            "key2": "value 123",
            "key3": None,
        }
        self.assertDictEqual(
            parse_json(
                json_str, mock_keyword_callback, required_fields, keywords
            ),
            {"123": 3, "value": 1},
        )
        self.assertEqual(mock_keyword_callback.call_count, 4)


if __name__ == "__main__":
    unittest.main()
