import unittest
import unittest.mock
from unittest.mock import MagicMock
from mtg_deck_editor.parsing.cards import MoxfieldParser


class TestMoxfieldParser(unittest.TestCase):
    def test_none_string(self):
        parser = MoxfieldParser()
        self.assertIsNone(parser.parse_string(None))

    def test_empty_string(self):
        parser = MoxfieldParser()
        self.assertIsNone(parser.parse_string(""))

    def test_quantity_and_name(self):
        parser = MoxfieldParser()
        card = parser.parse_string("23 This Is The Name")
        self.assertEqual(card.quantity, 23)
        self.assertEqual(card.name, "This Is The Name")

    def test_set_code_and_number(self):
        parser = MoxfieldParser()
        card = parser.parse_string("Name (USG) NUM1")
        self.assertEqual(card.set_code, "USG")
        self.assertEqual(card.collector_number, "NUM1")

    def test_lower_set_code(self):
        parser = MoxfieldParser()
        card = parser.parse_string("Name (usg) NUM1")
        self.assertEqual(card.set_code, "USG")
        self.assertEqual(card.collector_number, "NUM1")


    