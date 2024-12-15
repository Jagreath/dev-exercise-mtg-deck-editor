from re import compile as re_compile
from mtg_deck_editor.models.decks import Card

_moxfield_decklist_pattern = re_compile(r"(\s*(?P<quant>\d+)\s*)?(?P<name>[\d\w\s\-\,\'\/]+)(\((?P<set>[\d\w]{3,4})\)\s*)?((?P<num>[\d\w\-★]{1,7})\s*)?.*")

class CardParser:
    def parse_string(self, string: str) -> Card:
        return None

class MoxfieldParser(CardParser):
    def parse_string(self, string: str) -> Card:
        """
        Parse a string into components that match a moxfield pattern:
        "quant name (set) num"

        The set and number components are optional.

        Returns a dictionary containing as many keys as were found in the string.
        """
        match = _moxfield_decklist_pattern.match(string)
        if match and match.group("name"):
            card = Card()
            card.name = match.group("name").title().strip()
            card.quantity = int(match.group("quant").strip()) if match.group("quant") else 1
            if match.group("set"):
                card.set_code = match.group("set").upper()
            if match.group("num"):
                card.collector_number = match.group("num").upper()
            return card
        return None