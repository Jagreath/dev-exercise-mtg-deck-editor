from uuid import uuid4
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self):
        self.uuid: str = ""
        self.name: str = ""
        self.hash: str = ""
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created
        self.accessed: datetime = self.created
        self._decks: list[Deck] = []

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    @property
    def decks(self):
        return self._decks
    
    def add_deck(self, 
                 name: str, 
                 description: str = "") -> "Deck":
        deck = Deck()
        deck._user = self
        deck.user_uuid = self.uuid
        deck.uuid = str(uuid4())     
        deck.name = name
        deck.description = description

        self._decks.append(deck)
        return deck
    
    def validate_password(self, password: str) -> bool:
        if password and self.hash:
            return check_password_hash(self.hash, password)
        return False

    @staticmethod
    def new(name: str, password: str):
        if not name:
            raise ValueError("Name is required.")
        if not password:
            raise ValueError("Password is required.")

        user = User()
        user.uuid = str(uuid4())
        user.name = name
        user.hash = generate_password_hash(password)
        return user

class Deck:
    def __init__(self):
        self.uuid: str = ""
        self.user_uuid: str = ""
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created
        self._name: str = ""
        self.description: str = ""

        self._user: User = None
        self._cards: list[Card] = []

    def __repr__(self):
        return f"<Deck {self.name!r}>"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name is required.")

        self._name = value

    @property
    def cards(self):
        return (self._cards)

    def add_card(self,
                 uuid: str, 
                 name: str, 
                 set_code: str, 
                 collector_number: str, 
                 mana_cost: str, 
                 mana_value: str, 
                 type: str,
                 quantity: int = 1) -> "Card":
        if uuid not in [c.uuid for c in self._cards]:
            card = Card()
            card._deck = self
            card.deck_uuid = self.uuid
            card.uuid = uuid
            card.name = name.title()
            card.set_code = set_code.upper()
            card.collector_number = collector_number.upper()
            card.mana_cost = mana_cost
            card.mana_value = mana_value
            card.quantity = quantity
            card.card_type = type

            self.cards.append(card)
            return card
        return None

    @property
    def spells(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type != "land" and c.card_type != "creature"])
    
    @property
    def creatures(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type == "creature"])
    
    @property
    def lands(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type == "land"])

class Card:
    def __init__(self):
        self.deck_uuid: str = ""
        self.uuid: str = ""
        self.name: str = ""
        self.quantity: int = 1
        self.set_code: str = ""
        self.collector_number: str = ""
        self.mana_cost: str = ""
        self.mana_value: str = ""
        self.card_type: str = ""
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created

        self._deck: Deck = None

    def __repr__(self):
        return f"<Card {self.name} ({self.set_code}) [{self.collector_number}]>"