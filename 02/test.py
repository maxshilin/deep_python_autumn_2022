import unittest
import random
from unittest.mock import patch
from faker import Faker

from parse_json import parse_json


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()

        self.first_names = [*set(self.fake.first_name() for _ in range(30))]
        self.last_names = [*set(self.fake.last_name() for _ in range(30))]
        self.phone_number = [*set(self.fake.phone_number() for _ in range(90))]

        self.json = [
            {
                "json_str": {
                    "firstName": " ".join(self.first_names),
                    "lastName": " ".join(self.last_names),
                    "phoneNumber": " ".join(self.phone_number),
                },
                "required_fields": [
                    "firstName",
                    "lastName",
                    "phoneNumber",
                ],
                "keywords": random.sample(self.first_names, 10)
                + random.sample(self.last_names, 10)
                + random.sample(self.phone_number, 10),
                "call_number": 30,
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

        self.assertIsNone(parse_json("", mock_keyword_callback, [" "], [" "]))
        self.assertEqual(mock_keyword_callback.call_count, 0)

        self.assertEqual(
            parse_json(
                '{"key1": ""}',
                mock_keyword_callback,
                required_fields,
                keywords,
            ),
            {},
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
        mock_keyword_callback.call_count = 0

    @patch("json.loads")
    @patch("parse_json.keyword_callback")
    def test_faker_json(self, mock_keyword_callback, mock_json_loads):
        json_str = " "
        required_fields = self.json[0]["required_fields"]
        keywords = self.json[0]["keywords"]

        mock_json_loads.return_value = self.json[0]["json_str"]
        parse_json(json_str, mock_keyword_callback, required_fields, keywords)
        self.assertEqual(
            mock_keyword_callback.call_count, self.json[0]["call_number"]
        )
        mock_keyword_callback.call_count = 0


if __name__ == "__main__":
    unittest.main()
