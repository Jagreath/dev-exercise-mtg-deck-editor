from typing import List
from uuid import uuid4
import sqlalchemy as sa
import sqlalchemy.orm as sao
from mtg_deck_editor import db

class Deck(db.Model):
    __bind_key__ = "DECKS"
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
        

class Card(db.Model):
    __bind_key__ = "DECKS"
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, index=True)
    deck_uuid: sao.Mapped[str] = sao.mapped_column(sa.ForeignKey(Deck.uuid), primary_key=True, index=True)
    quantity: sao.Mapped[int] = sao.mapped_column(nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)
    set_code: sao.Mapped[str] = sao.mapped_column(nullable=False)
    collector_number: sao.Mapped[str] = sao.mapped_column(nullable=False)
    
    deck: sao.Mapped[Deck] = sao.relationship(back_populates="cards")

    def __repr__(self):
        return f'<Card {self.uuid!r} ({self.name} - {self.deck_uuid})>'