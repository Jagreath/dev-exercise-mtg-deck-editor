from datetime import datetime, timedelta, timezone
from mtg_deck_editor.services.dtos import CardDto

class RateLimit:
    def __init__(self, service : str ="None", count : int =0, limit_window : datetime =datetime.min):
        self.service = service
        self.count = count
        self.limit_window = limit_window

class ScryfallCache:
    def __init__(self, method_uri: str):
        self.id = 0
        self.method_uri = method_uri
        self.expiry = datetime.now(timezone.utc) + timedelta(days=1)
        self.cached_cards : list[CachedCard] = []

class CachedCard:
    def __init__(self, cache_id, id = "", name = "", mana_cost = "", set = "", collector_number = "", cmc = "", **kwargs):
        self.cache_id = cache_id
        self.id = id
        self.name = name
        self.mana_cost = mana_cost
        self.set = set
        self.collector_number = collector_number
        self.cmc = cmc
        self.sf_cache: ScryfallCache = None

    def dto(self):
        dto = CardDto()
        dto.__dict__.update(self.__dict__)
        return dto