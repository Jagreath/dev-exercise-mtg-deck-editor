import requests
import sqlalchemy as sa
import sqlalchemy.orm as sao
from datetime import datetime, timedelta
from mtg_deck_editor import db
from mtg_deck_editor.services.common import check_rate_limit

class CardDto:
    def __init__(self, 
                 id: str = "", 
                 cmc: int = 0, 
                 name: str = "", 
                 mana_cost: str = "", 
                 set: str = "", 
                 collector_number: str = ""):
        self.id = id
        self.cmc = cmc
        self.name = name
        self.mana_cost = mana_cost
        self.set = set
        self.collector_number = collector_number

class ScryfallCache(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, autoincrement=True)
    method_uri: sao.Mapped[str] = sao.mapped_column(nullable=False)
    expiry: sao.Mapped[datetime] = sao.mapped_column(nullable=False)

    cached_cards: sao.WriteOnlyMapped["CachedCard"] = sao.relationship(cascade="all,delete-orphan", passive_deletes=True)

    def __init__(self, method_uri: str):
        super().__init__()

        self.method_uri = method_uri
        self.expiry = datetime.now() + timedelta(days=1)

    def invalidate(self):
        db.session.delete(self)
        db.session.commit()

    def get_card(self) -> "CachedCard":
        return db.session.scalar(
            self.cached_cards.select().where(CachedCard.cache_id == self.id)
        )
    
    def cache_get_card_results(self, **kwargs) -> "CachedCard":
        cached_card = CachedCard(self.id, **kwargs)
        db.session.add(cached_card)
        db.session.commit()
        return cached_card
    
    def search_cards(self) -> list["CachedCard"]:
        return db.session.scalars(
            self.cached_cards.select().where(CachedCard.cache_id == self.id)
        ).fetchall()
    
    def cache_search_card_results(self, cards: list[dict]) -> list["CachedCard"]:
        cached_cards = [CachedCard(self.id, **c) for c in cards]
        db.session.add_all(cached_cards)
        db.session.commit()
        return cached_cards

    @staticmethod
    def get_cache(method_uri: str) -> "ScryfallCache":
        cache : ScryfallCache = db.session.execute(
            db.select(ScryfallCache)
            .where(ScryfallCache.method_uri == method_uri)).scalar()
        if cache is not None and datetime.now() > cache.expiry:
            cache.invalidate()
            cache = None
        if cache is None:
            cache = ScryfallCache(method_uri)
            db.session.add(cache)
            db.session.commit()
        return cache

class CachedCard(db.Model):
    cache_id: sao.Mapped[int] = sao.mapped_column(sa.ForeignKey(ScryfallCache.id), primary_key=True)
    id: sao.Mapped[str] = sao.mapped_column(primary_key=True)
    name: sao.Mapped[str] = sao.mapped_column()
    mana_cost : sao.Mapped[str] = sao.mapped_column()
    set : sao.Mapped[str] = sao.mapped_column()
    collector_number : sao.Mapped[str] = sao.mapped_column()
    cmc : sao.Mapped[int] = sao.mapped_column()

    cache: sao.Mapped[ScryfallCache] = sao.relationship(back_populates="cached_cards")

    def __init__(self, cache_id, id = "", name = "", mana_cost = "", set = "", collector_number = "", cmc = "", **kwargs):
        super().__init__()

        self.cache_id = cache_id
        self.id = id
        self.name = name
        self.mana_cost = mana_cost
        self.set = set
        self.collector_number = collector_number
        self.cmc = cmc

    def dto(self):
        dto = CardDto()
        dto.__dict__.update(self.__dict__)
        return dto

class ScryfallApi:
    def get_card(self, set_code: str, collector_number: str) -> CardDto:
        set_code = set_code.lower()
        method_uri = f'/cards/{set_code}/{collector_number}'
        cache = ScryfallCache.get_cache(method_uri)
        cached_card = cache.get_card()
        if cached_card is None:
            if check_rate_limit("scryfall", max_count=50, duration=1):
                resp = requests.get(f"https://api.scryfall.com{method_uri}", 
                                    headers={'user-agent': 'jag_mtg_deck_editor/0.0.1', 
                                                'Accept': 'application/json'})
                if resp.ok:
                    cached_card = cache.cache_get_card_results(**resp.json())
        return cached_card.dto()
    
    def search_cards(self, name: str, dir: str = 'asc', page: int = 1) -> list[CardDto]:
        method_uri = f'/cards/search?q={name}&dir={dir}&page={page}'
        cache = ScryfallCache.get_cache(method_uri)
        cached_cards = cache.search_cards()
        if cached_cards is None or len(cached_cards) < 1:
            if check_rate_limit("scryfall", max_count=50, duration=1):
                resp = requests.get(f"https://api.scryfall.com{method_uri}", 
                                    headers={'user-agent': 'jag_mtg_deck_editor/0.0.1', 
                                                'Accept': 'application/json'})
                if resp.ok:
                    cached_cards = cache.cache_search_card_results(resp.json()["data"])
        return [c.dto() for c in cached_cards]