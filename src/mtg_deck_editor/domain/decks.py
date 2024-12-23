from uuid import uuid4
from datetime import datetime
from mtg_deck_editor.services.dtos import CardDto

class Deck:
    def __init__(self, name="Lorem Ipsum Seasoning Salt", description=""):
        self.uuid: str = str(uuid4())
        self.name: str = name
        self.description: str = description
        self.created: datetime = datetime.now()
        self.modified: datetime = self.created
        self.cards: list[Card] = []

    def __repr__(self):
        return f'<Deck {self.name!r}>'

    def add_card(self, card: "Card"):
        if card.uuid not in [c.uuid for c in self.cards]:
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
        self.created: datetime = datetime.now()
        self.modified: datetime = self.created

        self.deck: Deck = None

    def __repr__(self):
        return f'<Card {self.uuid!r} ({self.name} - {self.deck_uuid})>'
    
    def copy_scryfall_dto(self, dto: CardDto):
        self.uuid = dto.id
        self.name = dto.name
        self.set_code = dto.set.upper()
        self.collector_number = dto.collector_number
        self.mana_cost = dto.mana_cost
        self.mana_value = dto.cmc