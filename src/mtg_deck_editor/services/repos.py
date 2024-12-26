from mtg_deck_editor.services.models import CachedCard, ScryfallCache

class BaseRateLimitRepository:
    def check_rate_limit(self, service_name, max_count = 10, duration = 1) -> bool:
        pass

class BaseScryfallCacheRepository:
    def get_cache(self, method_uri: str) -> ScryfallCache:
        pass

    def get_card(self, id) -> CachedCard:
        pass
    
    def cache_get_card_results(self, id, **kwargs) -> CachedCard:
        pass
    
    def search_cards(self, id) -> list[CachedCard]:
        pass
    
    def cache_search_card_results(self, id, cards: list[dict]) -> list[CachedCard]:
        pass