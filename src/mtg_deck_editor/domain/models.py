from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class ValidationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

@dataclass
class User:
    uuid: str
    name: str
    hash: str
    created: datetime
    modified: datetime
    accessed: datetime
    _decks: list["Deck"] = field(default_factory=list)

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    @property
    def decks(self) -> list["Deck"]:
        """A read-only list of decks."""
        return self._decks[:]
    
    def add_deck(self, 
                 name: str, 
                 description: str = "") -> "Deck":
        utcnow = datetime.now(timezone.utc)
        deck = Deck(_user = self, 
                    user_uuid=self.uuid,
                    uuid = str(uuid4()),
                    name = name,
                    description = description,
                    created=utcnow,
                    modified=utcnow)
        self._decks.append(deck)
        self.modified = utcnow
        return deck
    
    def validate_password(self, password: str) -> bool:
        if password and self.hash:
            return check_password_hash(self.hash, password)
        return False

    @staticmethod
    def new(name: str, password: str):
        if not name:
            raise ValidationError("Name is required.")
        if not password:
            raise ValidationError("Password is required.")

        utcnow = datetime.now(timezone.utc)
        hash = generate_password_hash(password)
        return User(uuid=str(uuid4()),
                    name=name,
                    created=utcnow,
                    modified=utcnow,
                    accessed=utcnow,
                    hash=hash)

@dataclass
class Deck:
    uuid: str
    user_uuid: str
    _name: str
    _description: str
    created: datetime
    modified: datetime
    _user: User
    _cards: list["Card"] = field(default_factory=list)

    def __repr__(self):
        return f"<Deck {self.name!r}>"
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValidationError("Name is required.")

        self._name = value.title()
        self.modified = datetime.now(timezone.utc)

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
        self.modified = datetime.now(timezone.utc)

    def add_card(self, 
                 name: str, 
                 quantity: int, 
                 set_code: str, 
                 collector_number: str, 
                 mana_cost: str, 
                 mana_value: str, 
                 card_type: str) -> "Card":
        if not name:
            raise ValidationError("A name is required.")
        if not mana_cost:
            raise ValidationError("A mana cost is required.")
        if not mana_value:
            raise ValidationError("A mana value is required.")
        if not card_type:
            raise ValidationError("A card type is required.")
        
        utcnow = datetime.now(timezone.utc)
        card = Card(_deck = self, 
                    deck_uuid=self.uuid,
                    mana_cost=mana_cost,
                    mana_value=mana_value,
                    card_type=card_type)
        card.name = name
        card.quantity = quantity
        card.set_code = set_code
        card.collector_number = collector_number
        card.created = utcnow
        card.modified = utcnow
        self._cards.append(card)
        self.modified = utcnow
        return card
    
    def remove_card(self, id: int):
        card = next((c for c in self._cards if c.id == id), None)
        if card is not None:
            self._cards.remove(card)
            self.modified = datetime.now(timezone.utc)

    @property
    def cards(self) -> list["Card"]:
        """A read-only list of cards."""
        return self._cards[:]

    @property
    def spells(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type != "land" and c.card_type != "creature"])
    
    @property
    def creatures(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type == "creature"])
    
    @property
    def lands(self) -> list["Card"]:
        return list([c for c in self._cards if c.card_type == "land"])

@dataclass
class Card:
    id: int
    deck_uuid: str
    _name: str
    _quantity: int
    _set_code: str
    _collector_number: str
    mana_cost: str
    mana_value: str
    card_type: str
    created: datetime
    modified: datetime
    _deck: Deck
    _tags: list["Tag"] = field(default_factory=list)

    def __repr__(self):
        return f"<Card {self.name} ({self.set_code}) [{self.collector_number}]>"
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value):
        if value:
            self._name = value.title()
            self.modified = datetime.now(timezone.utc)

    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int):
        if value is not None and self._quantity != value:
            if value < 1:
                value = 1
            self._quantity = value
            self.modified = datetime.now(timezone.utc)

    @property
    def set_code(self) -> str:
        return self._set_code
    
    @set_code.setter
    def set_code(self, value: str):
        if value and value != self._set_code:
            self._set_code = value.upper()
            self.modified = datetime.now(timezone.utc)

    @property
    def collector_number(self) -> str:
        return self._collector_number
    
    @collector_number.setter
    def collector_number(self, value):
        if value and value != self._collector_number:
            self._collector_number = value.upper()
            self.modified = datetime.now(timezone.utc)

    def add_tag(self, name: str) -> "Tag":
        if tag not in [t.name for t in self._tags]:
            tag = Tag(name=tag,
                      deck_uuid=self.deck_uuid, 
                      card_id=self.id,
                      _card=self)
            self._tags.append(tag)
            self.modified = datetime.now(timezone.utc)
            return tag
        return None

    def remove_tag(self, name:str):
        tag = next((t for t in self._tags if t.name == name), None)
        if tag is not None:
            self._tags.remove(tag)
            self.modified = datetime.now(timezone.utc)

    @property
    def tags(self) -> list["Tag"]:
        """A read-only list of tags."""
        return self._tags[:]

class Tag:
    name: str
    deck_uuid: str
    card_id: int
    _card: Card

    def __repr__(self):
        return f"<Tag {self.name}>"