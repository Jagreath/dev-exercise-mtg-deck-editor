from typing import Self
from re import compile as re_compile
from uuid import UUID, uuid4
import sqlalchemy as sa
import sqlalchemy.orm as sao
from . import db

_moxfield_decklist_pattern = re_compile(r"(\s*(?P<quantity>\d+)\s*)?(?P<name>[\d\w\s\-\,\'\/]+)(\((?P<set_code>[\d\w]{3,4})\)\s*)?((?P<collector_number>[\d\w\-★]{1,7})\s*)?.*")

class Deck(db.Model):
    __bind_key__ = "DECKS"
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)
    description: sao.Mapped[str] = sao.mapped_column(nullable=True)

    cards: sao.WriteOnlyMapped["Card"] = sao.relationship(foreign_keys="Card.deck_uuid", back_populates="deck", passive_deletes=True)

    def __init__(self, name="Lorem Ipsum Seasoning Salt", description=""):
        self.uuid = str(uuid4())
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Deck {self.name!r}>'
    
    def parse_moxfield_decklist(self, decklist: str) -> Self:
        """
        Parse a string and add cards.
        String format looks something like: 
        "4 this is a card name (SET) NUMBER"

        The set and number may be omitted.
        """
        if decklist is not None:
            for row in decklist.strip().splitlines():
                match = _moxfield_decklist_pattern.match(row)
                if match:
                    params = {
                        "name": ""
                    }
                    if match.group("name"):
                        params["name"] = match.group("name").strip().title()
                    if match.group("set_code"):
                        params["setCode"] = match.group("set_code").strip().upper()
                    if match.group("collector_number"):
                        params["number"] = match.group("collector_number").strip().upper()

                    set_card = db.session.execute(db.select(SetCard).filter_by(**params)).scalar()
                    if set_card:
                        card = Card(
                            deck_uuid = self.uuid,
                            uuid = set_card.uuid,
                            quantity = int(match.group("quantity").strip()) if match.group("quantity") else 1
                        )
                        self.cards.add(card)
        return self
        

class Card(db.Model):
    __bind_key__ = "DECKS"
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False, unique=True, index=True)
    deck_uuid: sao.Mapped[str] = sao.mapped_column(sa.ForeignKey(Deck.uuid), primary_key=True, nullable=False, index=True)
    quantity: sao.Mapped[int] = sao.mapped_column(nullable=False)
    
    deck: sao.Mapped[Deck] = sao.relationship(foreign_keys="Card.deck_uuid", back_populates="cards")
    # set_card: sao ["SetCard"] = sao.relationship(foreign_keys="Card.uuid", distinct_target_key="SetCard.uuid", viewonly=True)

    def __repr__(self):
        return f'<Card {self.uuid!r}>'

class Set(db.Model):
    __bind_key__ = "SETS"
    __tablename__ = "sets"
    code: sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)

    def __init__(self, code="000", name="The Null Set"):
        self.code = code
        self.name = name

    def __repr__(self):
        return f'<Set {self.name!r}>'

class SetCard(db.Model):
    __bind_key__ = "SETS"
    __tablename__ = "cards"
    uuid: sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name: sao.Mapped[str] = sao.mapped_column(nullable=False)
    asciiName: sao.Mapped[str] = sao.mapped_column(nullable=True)
    setCode: sao.Mapped[str] = sao.mapped_column(nullable=False)
    artist: sao.Mapped[str] = sao.mapped_column(nullable=True)
    borderColor: sao.Mapped[str] = sao.mapped_column(nullable=False)
    defense: sao.Mapped[str] = sao.mapped_column(nullable=True)
    duelDeck: sao.Mapped[str] = sao.mapped_column(nullable=True)
    edhrecRank: sao.Mapped[int] = sao.mapped_column(nullable=True)
    edhrecSaltiness: sao.Mapped[int] = sao.mapped_column(nullable=True)
    faceFlavorName: sao.Mapped[str] = sao.mapped_column(nullable=True)
    faceManaValue: sao.Mapped[int] = sao.mapped_column(nullable=True)
    faceName: sao.Mapped[str] = sao.mapped_column(nullable=True)
    flavorName: sao.Mapped[str] = sao.mapped_column(nullable=True)
    flavorText: sao.Mapped[str] = sao.mapped_column(nullable=True)
    frameVersion: sao.Mapped[str] = sao.mapped_column(nullable=False)
    hand: sao.Mapped[str] = sao.mapped_column(nullable=True)
    hasAlternativeDeckLimit: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    hasContentWarning: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    hasFoil: sao.Mapped[bool] = sao.mapped_column(nullable=False)
    hasNonFoil: sao.Mapped[bool] = sao.mapped_column(nullable=False)
    isAlternative: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isFullArt: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isFunny: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isOnlineOnly: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isOversized: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isPromo: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isRebalanced: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isReprint: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isReserved: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isStarter: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isStorySpotlight: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isTextless: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    isTimeshifted: sao.Mapped[bool] = sao.mapped_column(nullable=True)
    language: sao.Mapped[str] = sao.mapped_column(nullable=False)
    layout: sao.Mapped[str] = sao.mapped_column(nullable=False)
    life: sao.Mapped[str] = sao.mapped_column(nullable=True)
    loyalty: sao.Mapped[str] = sao.mapped_column(nullable=True)
    manaCost: sao.Mapped[str] = sao.mapped_column(nullable=True)
    manaValue: sao.Mapped[int] = sao.mapped_column(nullable=False)
    number: sao.Mapped[str] = sao.mapped_column(nullable=False)
    originalReleaseDate: sao.Mapped[str] = sao.mapped_column(nullable=True)
    originalText: sao.Mapped[str] = sao.mapped_column(nullable=True)
    originalType: sao.Mapped[str] = sao.mapped_column(nullable=True)
    power: sao.Mapped[str] = sao.mapped_column(nullable=True)
    rarity: sao.Mapped[str] = sao.mapped_column(nullable=False)
    securityStamp: sao.Mapped[str] = sao.mapped_column(nullable=True)
    side: sao.Mapped[str] = sao.mapped_column(nullable=True)
    signature: sao.Mapped[str] = sao.mapped_column(nullable=True)
    text: sao.Mapped[str] = sao.mapped_column(nullable=True)
    toughness: sao.Mapped[str] = sao.mapped_column(nullable=True)
    type: sao.Mapped[str] = sao.mapped_column(nullable=False)
    watermark: sao.Mapped[str] = sao.mapped_column(nullable=True)
    # artistIds: sao.Mapped[string[]] = sao.mapped_column()
    # attractionLights?: sao.Mapped[number[]] = sao.mapped_column()
    # availability: sao.Mapped[string[]] = sao.mapped_column()
    # boosterTypes?: sao.Mapped[string[]] = sao.mapped_column()
    # cardParts?: sao.Mapped[string[]] = sao.mapped_column()
    # colorIdentity: sao.Mapped[string[]] = sao.mapped_column()
    # colorIndicator?: sao.Mapped[string[]] = sao.mapped_column()
    # colors: sao.Mapped[string[]] = sao.mapped_column()
    # finishes: sao.Mapped[string[]] = sao.mapped_column()
    # foreignData?: sao.Mapped[ForeignData[]] = sao.mapped_column()
    # frameEffects?: sao.Mapped[string[]] = sao.mapped_column()
    # identifiers: sao.Mapped[Identifiers] = sao.mapped_column()
    # keywords?: sao.Mapped[string[]] = sao.mapped_column()   
    # leadershipSkills?: sao.Mapped[LeadershipSkills] = sao.mapped_column()
    # legalities: sao.Mapped[Legalities] = sao.mapped_column()
    # originalPrintings?: sao.Mapped[string[]] = sao.mapped_column()
    # otherFaceIds?: sao.Mapped[string[]] = sao.mapped_column()
    # printings?: sao.Mapped[string[]] = sao.mapped_column()
    # promoTypes?: sao.Mapped[string[]] = sao.mapped_column()
    # purchaseUrls: sao.Mapped[PurchaseUrls] = sao.mapped_column()
    # relatedCards?: sao.Mapped[RelatedCards] = sao.mapped_column()
    # rebalancedPrintings?: sao.Mapped[string[]] = sao.mapped_column()
    # rulings?: sao.Mapped[Rulings[]] = sao.mapped_column()
    # sourceProducts?: sao.Mapped[SourceProducts] = sao.mapped_column()
    # subsets?: sao.Mapped[string[]] = sao.mapped_column()
    # subtypes: sao.Mapped[string[]] = sao.mapped_column()
    # supertypes: sao.Mapped[string[]] = sao.mapped_column()
    # types: sao.Mapped[string[]] = sao.mapped_column()
    # variations?: sao.Mapped[string[]] = sao.mapped_column()

    def __init__(self):
        pass

    def __repr__(self):
        return f'<SetCard {self.name!r}>'
    
