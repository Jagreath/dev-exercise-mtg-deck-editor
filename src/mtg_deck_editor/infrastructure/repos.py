from mtg_deck_editor.infrastructure import db
from mtg_deck_editor.domain.models import User, Deck
from mtg_deck_editor.services.models import RateLimit, ScryfallCache, CachedCard
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
    
class UserRepository:
    def get_by_uuid(self, uuid):
        return db.session.execute(select(User).filter(User.uuid == uuid)).scalar_one_or_none()
    
    def get_by_name(self, name):
        return db.session.execute(select(User).filter(User.name == name)).scalar_one_or_none()
    
    def get_all(self):
        return db.session.execute(select(User).order_by(User.name)).scalars()
    
    def add(self, user: User):
        db.session.add(user)
    
    def save(self):
        db.session.commit()

class DeckRepository:

    def get(self, uuid: str) -> Deck:
        return db.session.execute(select(Deck).filter(Deck.uuid == uuid)).scalar_one_or_none()
    
    def get_all(self) -> list[Deck]:
        return db.session.execute(select(Deck).order_by(Deck.name)).scalars()

    def add(self, deck: Deck):
        db.session.add(deck)
    
    def save(self):
        db.session.commit()
    
    def delete(self, deck: Deck):
        db.session.delete(deck)

class ScryfallCacheRepository:

    def get_cache(self, method_uri: str) -> ScryfallCache:
        cache : ScryfallCache = self.session.execute(
            select(ScryfallCache)
            .where(ScryfallCache.method_uri == method_uri)).scalar()
        if cache is not None and datetime.now(timezone.utc) > cache.expiry:
            db.session.delete(cache)
            db.session.commit()
            cache = None
        if cache is None:
            cache = ScryfallCache(method_uri)
            db.session.add(cache)
            db.session.commit()
        return cache

    def get_card(self, id):
        return db.session.execute(select(CachedCard).where(CachedCard.cache_id == id)).scalar_one_or_none()
    
    def cache_get_card_results(self, id, **kwargs) -> CachedCard:
        cached_card = CachedCard(id, **kwargs)
        db.session.add(cached_card)
        db.session.commit()
        return cached_card
    
    def search_cards(self, id) -> list[CachedCard]:
        return db.session.execute(
            select(CachedCard).where(CachedCard.cache_id == id)
        ).scalars()
    
    def cache_search_card_results(self, id, cards: list[dict]) -> list[CachedCard]:
        cached_cards = [CachedCard(id, **c) for c in cards]
        db.session.add_all(cached_cards)
        db.session.commit()
        return cached_cards

class RateLimitRepository:
    def check_rate_limit(self, service_name, max_count=10, duration=1) -> bool:
        with db.session.begin_nested() as st:
            rl_entry = db.session.execute(
                select(RateLimit)
                .filter(RateLimit.service == service_name)).scalar()
            if rl_entry is None:
                rl_entry = RateLimit(service=service_name, limit_window=(datetime.now(timezone.utc) + timedelta(seconds=duration)))
                db.session.add(rl_entry)
            if rl_entry.limit_window < datetime.now(timezone.utc):
                rl_entry.count = 0
                rl_entry.limit_window = datetime.now(timezone.utc) + timedelta(seconds=duration)
            if rl_entry.count < max_count:
                rl_entry.count += 1
                st.commit()
                return True
            return False

    # def allow_wait(service_name, max_count = 10, duration = 1, timeout = 10):
    #     start_time = datetime.now(timezone.utc)
    #     while not allow(service_name, max_count, duration):
    #         if (datetime.now(timezone.utc) - start_time).seconds > timeout:
    #             raise "Timeout"
    #         time.sleep(duration) # or something, I don't know