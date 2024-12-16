import requests
import sqlalchemy as sa
import sqlalchemy.orm as sao
from mtg_deck_editor import db
from mtg_deck_editor.services.common import ServiceCache, allow


class GetCardCached(db.Model):
    cache_id: sao.Mapped[int] = sao.mapped_column(sa.ForeignKey(ServiceCache.id), primary_key=True)
    id : sao.Mapped[str] = sao.mapped_column(primary_key=True, nullable=False)
    name : sao.Mapped[str] = sao.mapped_column()
    mana_cost : sao.Mapped[str] = sao.mapped_column()
    set : sao.Mapped[str] = sao.mapped_column()
    collector_number : sao.Mapped[str] = sao.mapped_column()
    cmc : sao.Mapped[int] = sao.mapped_column()

    # cache: sao.Mapped[ScryfallCache] = sao.relationship(back_populates="cards")

    def __init__(self, id = "", name = "", mana_cost = "", set = "", collector_number = "", cmc = "", **kwargs):
        super().__init__()

        self.id = id
        self.name = name
        self.mana_cost = mana_cost
        self.set = set
        self.collector_number = collector_number
        self.cmc = cmc

    @staticmethod
    def get_card(set_code: str, collector_number: str) -> "GetCardCached":
        s_cache = ServiceCache.get_or_default(ScryfallApi.__name__, f"/cards/{set_code}/{collector_number}")
        return db.session.execute(db.select(GetCardCached).filter(GetCardCached.cache_id == s_cache.id)).scalar()
    
    @staticmethod
    def cache(**kwargs) -> "GetCardCached":
        cache_row = GetCardCached(**kwargs)
        s_cache = ServiceCache.get_or_default(ScryfallApi.__name__, f"/cards/{cache_row.set}/{cache_row.collector_number}")
        cache_row.cache_id = s_cache.id
        db.session.add(cache_row)
        db.session.commit()
        return cache_row


class ScryfallApi:
    def get_card(self, set_code: str, collector_number: str) -> GetCardCached:
        set_code = set_code.lower()
        card = GetCardCached.get_card(set_code, collector_number)
        if card is None:
            if allow("scryfall", max_count=50, duration=1):
                resp = requests.get(f"https://api.scryfall.com/cards/{set_code}/{collector_number}", 
                                    headers={'user-agent': 'jag_mtg_deck_editor/0.0.1', 
                                                'Accept': 'application/json'})
                if resp.ok:
                    card = GetCardCached.cache(**resp.json())
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