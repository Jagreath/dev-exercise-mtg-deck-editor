from mtg_deck_editor.app import db
from mtg_deck_editor.domain.decks import Deck
from mtg_deck_editor.domain.repos import BaseDeckRepository, DeckRepositoryFactory
from mtg_deck_editor.services.models import RateLimit, ScryfallCache, CachedCard
from mtg_deck_editor.services.repos import BaseRateLimitRepository, BaseScryfallCacheRepository, ScryfallCacheRepositoryFactory
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
    
class DeckRepository(BaseDeckRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, uuid: str) -> Deck:
        return self.session.execute(select(Deck).filter(Deck.uuid == uuid)).scalar_one_or_none()
    
    def get_all(self) -> list[Deck]:
        return self.session.execute(select(Deck).order_by(Deck.name)).scalars()

    def add(self, deck: Deck):
        self.session.add(deck)
    
    def save(self):
        self.session.commit()
    
    def delete(self, deck: Deck):
        self.session.delete(deck)

class ContextDeckRepositoryFactory(DeckRepositoryFactory):
    def create(self) -> BaseDeckRepository:
        return DeckRepository(db.session)

class ScryfallCacheRepository(BaseScryfallCacheRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_cache(self, method_uri: str) -> ScryfallCache:
        cache : ScryfallCache = self.session.execute(
            select(ScryfallCache)
            .where(ScryfallCache.method_uri == method_uri)).scalar()
        if cache is not None and datetime.now() > cache.expiry:
            self.session.delete(cache)
            self.session.commit()
            cache = None
        if cache is None:
            cache = ScryfallCache(method_uri)
            self.session.add(cache)
            self.session.commit()
        return cache

    def get_card(self, id):
        return self.session.execute(select(CachedCard).where(CachedCard.cache_id == id)).scalar_one_or_none()
    
    def cache_get_card_results(self, id, **kwargs) -> CachedCard:
        cached_card = CachedCard(id, **kwargs)
        self.session.add(cached_card)
        self.session.commit()
        return cached_card
    
    def search_cards(self, id) -> list[CachedCard]:
        return self.session.execute(
            select(CachedCard).where(CachedCard.cache_id == id)
        ).scalars()
    
    def cache_search_card_results(self, id, cards: list[dict]) -> list[CachedCard]:
        cached_cards = [CachedCard(id, **c) for c in cards]
        self.session.add_all(cached_cards)
        self.session.commit()
        return cached_cards
    
class ContextScryfallCacheRepositoryFactory(ScryfallCacheRepositoryFactory):
    def create(self) -> "ScryfallCacheRepository":
        return ScryfallCacheRepository(db.session)

class RateLimitRepository(BaseRateLimitRepository):
    def __init__(self, session: Session):
        self.session = session

    def check_rate_limit(self, service_name, max_count=10, duration=1) -> bool:
        with self.session.begin_nested() as st:
            rl_entry = self.session.execute(
                select(RateLimit)
                .filter(RateLimit.service == service_name)).scalar()
            if rl_entry is None:
                rl_entry = RateLimit(service=service_name, limit_window=(datetime.now() + timedelta(seconds=duration)))
                self.session.add(rl_entry)
            if rl_entry.limit_window < datetime.now():
                rl_entry.count = 0
                rl_entry.limit_window = datetime.now() + timedelta(seconds=duration)
            if rl_entry.count < max_count:
                rl_entry.count += 1
                st.commit()
                return True
            return False

    # def allow_wait(service_name, max_count = 10, duration = 1, timeout = 10):
    #     start_time = datetime.now()
    #     while not allow(service_name, max_count, duration):
    #         if (datetime.now() - start_time).seconds > timeout:
    #             raise "Timeout"
    #         time.sleep(duration) # or something, I don't know

class ContextRateLimitRepositoryFactory:
    def create(self) -> RateLimitRepository:
        return RateLimitRepository(db.session)