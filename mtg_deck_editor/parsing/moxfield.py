from ..models.decks import Card

from re import compile as re_compile
_moxfield_decklist_pattern = re_compile(r"(\s*(?P<quant>\d+)\s*)?(?P<name>[\d\w\s\-\,\'\/]+)(\((?P<set>[\d\w]{3,4})\)\s*)?((?P<num>[\d\w\-★]{1,7})\s*)?.*")

class MoxfieldParser:

    def parse_string(self, moxfield_str: str) -> Card:
        """
        Parse a string into components that match a moxfield pattern:
        "{QUANT_COL} {NAME_COL} ({SET_COL}) {QUANT_COL}"

        The set and number components are optional.

        Returns a dictionary containing as many keys as were found in the string:
        {NAME_COL}, {SET_COL}, {NUM_COL}
        """
        match = _moxfield_decklist_pattern.match(moxfield_str)
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
    
    def parse_lines(self, moxfield_lines: str) -> list[Card]:
        cards = []
        if moxfield_lines:
            for line in moxfield_lines.strip().splitlines():
                cards.append(self.parse_string(line))
        return cards