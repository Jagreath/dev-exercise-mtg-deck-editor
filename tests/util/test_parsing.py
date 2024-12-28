import logging
import unittest
from mtg_deck_editor.util.parsing import parse_moxfield_string

logger = logging.getLogger(__name__)

class TestMoxfieldParser(unittest.TestCase):
    def test_none_string(self):
        self.assertIsNone(parse_moxfield_string(None))

    def test_empty_string(self):
        self.assertIsNone(parse_moxfield_string(""))

    def test_matching_string(self):
        name, set_code, collector_number, quantity = parse_moxfield_string("23 This Is The Name (SET) NUMBER")
        self.assertEqual(quantity, 23)
        self.assertEqual(name, "This Is The Name")
        self.assertEqual(set_code, "SET")
        self.assertEqual(collector_number, "NUMBER")


    