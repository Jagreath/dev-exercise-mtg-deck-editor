from typing import List
from uuid import uuid4
import sqlalchemy as sa
import sqlalchemy.orm as sao
from mtg_deck_editor import db
from mtg_deck_editor.services.scryfall import ScryfallCard

class Deck(db.Model):
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)
    description: sao.Mapped[str] = sao.mapped_column(nullable=True)

    cards: sao.Mapped[List["Card"]] = sao.relationship(back_populates="deck", cascade="all,delete-orphan")

    def __init__(self, name="Lorem Ipsum Seasoning Salt", description=""):
        self.uuid = str(uuid4())
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Deck {self.name!r}>'
    
    @staticmethod
    def get(uuid: str):
        return db.get_or_404(Deck, uuid)

    @staticmethod
    def get_all():
        return db.session.execute(db.select(Deck).order_by(Deck.name)).scalars()
    
    @staticmethod
    def new():
        deck = Deck()
        db.session.add(deck)
        return deck

    def add_card(self, card: "Card"):
        if card.uuid not in [c.uuid for c in self.cards]:
            self.cards.append(card)

    def delete(self):
        db.session.delete(self)

    def save(self):
        db.session.commit()

class Card(db.Model):
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, index=True)
    deck_uuid: sao.Mapped[str] = sao.mapped_column(sa.ForeignKey(Deck.uuid), primary_key=True, index=True)
    quantity: sao.Mapped[int] = sao.mapped_column(nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)
    set_code: sao.Mapped[str] = sao.mapped_column(nullable=False)
    collector_number: sao.Mapped[str] = sao.mapped_column(nullable=False)
    mana_cost: sao.Mapped[str] = sao.mapped_column(nullable=True)
    mana_value: sao.Mapped[int] = sao.mapped_column(nullable=False)
    
    deck: sao.Mapped[Deck] = sao.relationship(back_populates="cards")
    tags: sao.Mapped[List["Tag"]] = sao.relationship(back_populates="card", cascade="all,delete-orphan")

    def __repr__(self):
        return f'<Card {self.uuid!r} ({self.name} - {self.deck_uuid})>'
    
    def copy_scryfall_card(self, s_card: ScryfallCard):
        self.uuid = s_card.id
        self.name = s_card.name
        self.set_code = s_card.set
        self.collector_number = s_card.collector_number
        self.mana_cost = s_card.mana_cost
        self.mana_value = s_card.cmc

    
class Tag(db.Model):
    name: sao.Mapped[str] = sao.mapped_column(primary_key=True, index=True)
    card_uuid: sao.Mapped[str] = sao.mapped_column(sa.ForeignKey(Card.uuid), primary_key=True, index=True)
    deck_uuid: sao.Mapped[str] = sao.mapped_column(sa.ForeignKey(Deck.uuid), primary_key=True, index=True)
    
    card: sao.Mapped[Card] = sao.relationship(back_populates="tags")

def __repr__(self):
        return f'<Tag {self.name!r}>'