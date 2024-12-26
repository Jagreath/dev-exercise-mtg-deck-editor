from uuid import uuid4
from datetime import datetime, timezone
from mtg_deck_editor.services.dtos import CardDto
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name: str, password: str):
        if not name:
            raise ValueError("Name is required.")
        if not password:
            raise ValueError("Password is required.")

        self.uuid: str = str(uuid4())
        self.name: str = name
        self.hash: str = generate_password_hash(password)
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created
        self.decks: list[Deck] = []

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    def validate_password(self,password: str) -> bool:
        return check_password_hash(self.hash, password)
    
    def add_deck(self, deck: "Deck"):
        self.decks.append(deck)


class Deck:
    def __init__(self, name: str = "Lorem Ipsum"):
        self.uuid: str = str(uuid4())
        self.user_uuid: str = ""
        self.description: str = ""
        self.name: str = name
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created

        self.user: User = None
        self.cards: list[Card] = []

    def __repr__(self):
        return f"<Deck {self.name!r}>"
    
    def set_name(self, name: str):
        if not name:
            raise ValueError("Name is required.")
        
        self.name = name

    def add_card(self, card: "Card"):
        if card.uuid not in [c.uuid for c in self.cards]:
            #card.deck = self
            self.cards.append(card)

class Card:
    def __init__(self, uuid: str = "", deck_uuid: str = "", name: str = "None"):
        self.uuid = uuid
        self.deck_uuid = deck_uuid
        self.name = name
        self.set_code = ""
        self.collector_number = ""
        self.mana_cost = ""
        self.mana_value = ""
        self.quantity = 0
        self.created: datetime = datetime.now(timezone.utc)
        self.modified: datetime = self.created

        self.deck: Deck = None

    def __repr__(self):
        return f"<Card {self.uuid!r} ({self.name} - {self.deck_uuid})>"
    
    def copy_scryfall_dto(self, dto: CardDto):
        self.uuid = dto.id
        self.name = dto.name
        self.set_code = dto.set.upper()
        self.collector_number = dto.collector_number
        self.mana_cost = dto.mana_cost
        self.mana_value = dto.cmc