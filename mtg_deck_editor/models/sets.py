import sqlalchemy as sa
import sqlalchemy.orm as sao
from .. import db

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
    
