import unittest
import unittest.mock
from mtg_deck_editor.domain.models import User, Deck

class TestUser(unittest.TestCase):
    @unittest.mock.patch("mtg_deck_editor.domain.models.generate_password_hash", )
    def test_normal_create(self, generate_password_hash_mock: unittest.mock.MagicMock):
        generate_password_hash_mock.return_value = "ABC"

        user = User.new("test", "apassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "test")
        self.assertIsNotNone(user.uuid)

        generate_password_hash_mock.assert_called()
        self.assertEqual(user.hash, "ABC")

    def test_create_with_none_name(self):
        with self.assertRaises(ValueError):
            User.new(None, "")

    def test_create_with_empty_name(self):
        with self.assertRaises(ValueError):
            User.new("", "")

    def test_create_with_none_password(self):
        with self.assertRaises(ValueError):
            User.new("name", None)

    def test_create_with_empty_password(self):
        with self.assertRaises(ValueError):
            User.new("name", "")

    @unittest.mock.patch("mtg_deck_editor.domain.models.check_password_hash", )
    def test_validate_password_missing_hash(self, check_password_hash_mock: unittest.mock.MagicMock):
        check_password_hash_mock.return_value = True

        user = User()
        user.name = "name"
        user.hash = None
        self.assertFalse(user.validate_password("pass"))
        user.hash = ""
        self.assertFalse(user.validate_password("pass"))

        check_password_hash_mock.assert_not_called()

    @unittest.mock.patch("mtg_deck_editor.domain.models.check_password_hash", )
    def test_validate_password_missing_pass(self, check_password_hash_mock: unittest.mock.MagicMock):
        check_password_hash_mock.return_value = True

        user = User()
        user.name = "name"
        user.hash = "hash"
        self.assertFalse(user.validate_password(""))
        self.assertFalse(user.validate_password(None))
        
        check_password_hash_mock.assert_not_called()

    @unittest.mock.patch("mtg_deck_editor.domain.models.check_password_hash", )
    def test_validate_password_check(self, check_password_hash_mock: unittest.mock.MagicMock):
        check_password_hash_mock.return_value = False

        user = User()
        user.name = "name"
        user.hash = "hash"
        self.assertFalse(user.validate_password("pass"))
        
        check_password_hash_mock.assert_called()

    def test_add_deck_default(self):
        user = User()
        user.uuid = "UUID"
        deck = user.add_deck("test", "a default description")
        self.assertEqual(deck.user_uuid, user.uuid)
        self.assertEqual(1, len(user.decks))

class TestDeck(unittest.TestCase):
    def test_can_add_card(self):
        deck = Deck()
        card = deck.add_card("uuid", "name", "setcode", "num", "123", "1", "type", 0)
        self.assertIsNotNone(card)
        self.assertGreater(len(deck.cards), 0)

    def test_can_only_add_card_once(self):
        deck = Deck()
        card = deck.add_card("uuid", "name", "setcode", "num", "123", "1", "type", 0)
        card = deck.add_card("uuid", "name", "setcode", "num", "123", "1", "type", 0)
        self.assertEqual(len(deck.cards), 1)

    def test_set_name_default(self):
        deck = Deck()
        deck.name = "test"
        self.assertEqual(deck.name, "test")

    def test_set_empty_name(self):
        deck = Deck()
        with self.assertRaises(ValueError):
            deck.name = ""
        with self.assertRaises(ValueError):
            deck.name = None

    def test_set_description_default(self):
        deck = Deck()
        deck.description = "test"
        self.assertEqual("test", deck.description)

    def test_set_empty_description(self):
        deck = Deck()
        deck.description = ""
        deck.description = None
            
