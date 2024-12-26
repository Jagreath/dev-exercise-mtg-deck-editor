import unittest
import unittest.mock
from unittest.mock import MagicMock
from mtg_deck_editor.parsing.moxfield import MoxfieldParser


class TestMoxfieldParser(unittest.TestCase):
    def test_none_string(self):
        parser = MoxfieldParser()
        self.assertIsNone(parser.parse_string(None))

    def test_empty_string(self):
        parser = MoxfieldParser()
        self.assertIsNone(parser.parse_string(""))

    def test_matching_string(self):
        parser = MoxfieldParser()
        card = parser.parse_string("23 This Is The Name (SET) NUMBER")
        self.assertEqual(card.quantity, 23)
        self.assertEqual(card.name, "This Is The Name")
        self.assertEqual(card.set_code, "SET")
        self.assertEqual(card.collector_number, "NUMBER")


    