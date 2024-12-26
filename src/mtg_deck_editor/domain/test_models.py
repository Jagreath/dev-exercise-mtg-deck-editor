import unittest
import unittest.mock
from unittest.mock import MagicMock

from mtg_deck_editor.domain.models import Deck, Card
from mtg_deck_editor.services.dtos import CardDto

class TestDeck(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_can_create_deck(self):
        Deck()
        self.assertTrue(True)

    def test_can_add_card(self):
        deck = Deck()
        deck.add_card(Card("","",""))
        self.assertGreater(len(deck.cards), 0)

    def test_can_only_add_card_once(self):
        deck = Deck()
        card = Card("","","")
        card.uuid = "ABC"
        deck.add_card(card)
        deck.add_card(card)
        self.assertEqual(len(deck.cards), 1)

class TestCard(unittest.TestCase):
    def test_can_create_card(self):
        Card("","","")
        self.assertTrue(True)

    def test_copy_dto(self):
        card = Card("","","")
        dto = CardDto("id", 1, "name", "cost", "set", "num")
        card.copy_scryfall_dto(dto)
        self.assertEqual(card.uuid, dto.id)
        self.assertEqual(card.name, dto.name)
        self.assertEqual(card.mana_cost, dto.mana_cost)
        self.assertEqual(card.set_code, dto.set.upper())
        self.assertEqual(card.collector_number, dto.collector_number)
