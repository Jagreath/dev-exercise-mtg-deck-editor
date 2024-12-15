import requests
import sqlalchemy as sa
import sqlalchemy.orm as sao
from datetime import datetime
from mtg_deck_editor import db

class ScryfallCache(db.Model):
    id : sao.Mapped[int] = sao.mapped_column(primary_key=True, autoincrement=True)
    api_method : sao.Mapped[str] = sao.mapped_column(unique=True, nullable=False)
    expiry : sao.Mapped[datetime] = sao.mapped_column(nullable=False)

    cards: sao.WriteOnlyMapped["ScryfallCard"] = sao.relationship(back_populates="cache", cascade="all,delete-orphan", passive_deletes=True)

    def __init__(self, api_method : str, expiry: datetime = datetime.now()):
        super().__init__()

        self.api_method = api_method
        self.expiry = expiry

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(method_name: str) -> "ScryfallCache":
        return db.session.execute(
            db.select(ScryfallCache)
            .filter(ScryfallCache.api_method == method_name)).scalar()
    
    @staticmethod
    def cache_response(api_method: str):
        cache = ScryfallCache(api_method)
        db.session.add(cache)
        db.session.commit()
        return cache
    



class ScryfallCard(db.Model):
    cache_id: sao.Mapped[int] = sao.mapped_column(sa.ForeignKey(ScryfallCache.id), primary_key=True)
    id : sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name : sao.Mapped[str] = sao.mapped_column()
    mana_cost : sao.Mapped[str] = sao.mapped_column()
    set : sao.Mapped[str] = sao.mapped_column()
    collector_number : sao.Mapped[str] = sao.mapped_column()
    cmc : sao.Mapped[int] = sao.mapped_column()

    cache: sao.Mapped[ScryfallCache] = sao.relationship(back_populates="cards")

    def __init__(self, id = "", name = "", mana_cost = "", set = "", collector_number = "", cmc = "", **kwargs):
        super().__init__()

        self.id = id
        self.name = name
        self.mana_cost = mana_cost
        self.set = set.upper()
        self.collector_number = collector_number
        self.cmc = cmc

    @staticmethod
    def cache_card(cache_id = 0, **kwargs):
        card = ScryfallCard(**kwargs)
        card.cache_id = cache_id
        db.session.add(card)
        db.session.commit()
        return card

    @staticmethod
    def get(cache_id: int):
        return db.session.execute(
            db.select(ScryfallCard)
            .filter(ScryfallCard.cache_id == cache_id)).scalar()
        


class ScryfallApi:
    def get_card(self, set_code: str, collector_number: str) -> ScryfallCard:
        method_name = f"/cards/{set_code.lower()}/{collector_number}"
        cache = ScryfallCache.get(method_name)
        
        card = None
        if cache is None or (datetime.now() - cache.expiry).days > 1:
            if cache is not None:
                cache.delete()

            resp = requests.get("https://api.scryfall.com" + method_name, 
                                headers={'user-agent': 'jag_mtg_deck_editor/0.0.1', 
                                            'Accept': 'application/json'})
            if resp.ok:
                cache = ScryfallCache.cache_response(method_name)
                card = ScryfallCard.cache_card(cache_id=cache.id, **resp.json())
        else:
            card = ScryfallCard.get(cache.id)
            
        return card

    # def search_cards(self, q: str, dir: str = 'asc', page: int = 1):
    #     with get_cache() as cache:
    #         method_name = f'/cards/search/{q}/{dir}/{page}'
    #         cursor = cache.cursor()
    #         cache_entry = cursor.execute(
    #             "select method, expiry from cache where method = ? ", 
    #             [method_name]).fetchone()
            
    #         cards = []

    #         if (datetime.now() - cache_entry.expiry).days > 1:
    #             delete_cache_entry(cursor, method_name)
    #             # fetch from api
    #             insert_cache_entry(cursor, method_name)
    #         else:
    #             rows = cursor.execute("select * from get_card where set_code = ? and collector_number = ?").fetchall()
    #             cards = [CardDto(**r) for r in rows]

    #         return cards