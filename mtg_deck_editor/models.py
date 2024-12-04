from datetime import datetime
import re

class Set:
    def __init__(self, set_name: str = "Unknown", set_code: str = "000"):
        self.name = set_name
        self.code = set_code

    def __str__(self):
        return f'{self.name} [{self.code}]'
    
    def __repr__(self):
        return self.__str__()

class AtomicCard:
    def __init__(self, 
                 uuid: str = "00000000-0000-0000-0000-000000000000", 
                 name: str = "Unknown", 
                 collector_number: str = "",
                 set_code: str = "",
                 **kwargs):
        self.uuid = uuid
        self.name = name
        self.set_code = set_code
        self.collector_number = collector_number
        self.set = set if set else Set()

    def __str__(self):
        return f'{self.name} ({self.uuid}) [{self.set_code}] [{self.collector_number}]'

    def __repr__(self):
        return self.__str__()
    
    def json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'set_code': self.set_code,
            'collector_number': self.collector_number
        }
    
_card_parse_pattern = re.compile(r"(\s*(?P<quantity>\d+)\s*)?(?P<name>[\d\w\s\-\,\'\/]+)(\((?P<set_code>[\d\w]{3,4})\)\s*)?((?P<collector_number>[\d\w\-★]{1,7})\s*)?.*")

class DeckCard(AtomicCard):
    def __init__(self,
                 deck_id: int = -1,
                 quantity: int = 1,
                 **kwargs):
        super().__init__(**kwargs)

        self.deck_id = deck_id
        self.quantity = quantity
        self.tags = []

    def parse_and_replace(self, card_str: str):
        """
        Parse a string and fill this object's fields with the result.
        String format looks something like: 
        "4 this is a card name (SET) NUMBER"

        The set and number may be omitted.
        """
        if card_str is not None:
            match = _card_parse_pattern.match(card_str)
            if match:
                if match.group("quantity"):
                    self.quantity = int(match.group("quantity").strip())
                if match.group("name"):
                    self.name = match.group("name").strip().title()
                if match.group("set_code"):
                    self.set_code = match.group("set_code").strip().upper()
                if match.group("collector_number"):
                    self.collector_number = match.group("collector_number").strip().upper()
        return self

    def json(self):
        d = super().json()
        d.update({
            'deck_id': self.deck_id,
            'quantity': self.quantity
        })
        return d

class Deck():
    def __init__(self,
                 id: int = -1,
                 name: str = "",
                 description: str = "",
                 format: str = "",
                 created: datetime = None,
                 changed: datetime = None,
                 **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.format = format
        self.created = datetime.now() if created is None else created
        self.changed = datetime.now() if changed is None else changed
        self.cards = []

    def parse_and_replace_cards(self, cards_str: str):
        """
        Parses and replaces cards in this object with new objects based on the parsed string.
        """
        if cards_str is not None:
            self.cards = []
            for c_str in cards_str.strip().splitlines():
                self.cards.append(DeckCard(deck_id=self.id).parse_and_replace(c_str))
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'format': self.format,
            'created': self.created.isoformat(),
            'changed': self.changed.isoformat(),
            'cards': [c.to_dict() for c in self.cards]
        }
