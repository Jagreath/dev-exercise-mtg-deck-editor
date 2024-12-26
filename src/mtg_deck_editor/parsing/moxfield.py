from re import compile as re_compile
from mtg_deck_editor.domain.models import Card

_moxfield_decklist_pattern = re_compile(r"\s*(?P<quant>\d+)\s+(?P<name>[\d\w\s\-\,\'\/]+)\s+\((?P<set>[\d\w]{3,4})\)\s+(?P<num>[\d\w\-★]{1,7})\s*")

class MoxfieldParser:
    def parse_string(self, string: str) -> Card:
        """
        Parse a string into components that match a moxfield pattern:
        "quant name (set) num"
        Then return a Card with the parsed values.
        """
        if string is not None:
            match = _moxfield_decklist_pattern.match(string)
            if match:
                card = Card()
                card.name = match.group("name").title().strip()
                card.quantity = int(match.group("quant").strip())
                card.set_code = match.group("set").upper()
                card.collector_number = match.group("num").upper()
                return card
        return None