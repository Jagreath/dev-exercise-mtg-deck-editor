import requests
from mtg_deck_editor.infrastructure.repos import RateLimitRepository, ScryfallCacheRepository
from mtg_deck_editor.services.dtos import CardDto

USER_AGENT = "jag_mtg_deck_editor/0.0.1"
API_BASE_URI = "https://api.scryfall.com"
ACCEPTS = "application/json"

class ScryfallApi:
    def get_card(self, set_code: str, collector_number: str) -> CardDto:
        repo = ScryfallCacheRepository()
        rate_repo = RateLimitRepository()

        set_code = set_code.lower()
        method_uri = f"/cards/{set_code}/{collector_number}"
        cache = repo.get_cache(method_uri)
        cached_card = repo.get_card(cache.id)
        if cached_card is None:
            if rate_repo.check_rate_limit("scryfall", max_count=50, duration=1):
                resp = requests.get(f"{API_BASE_URI}{method_uri}", 
                                    headers={"user-agent": USER_AGENT, 
                                                "Accept": ACCEPTS})
                if resp.ok:
                    cached_card = repo.cache_get_card_results(cache.id, **resp.json())
        return cached_card.dto()
    
    def search_cards(self, name: str, dir: str = "asc", page: int = 1) -> list[CardDto]:
        repo = ScryfallCacheRepository()
        rate_repo = RateLimitRepository()

        method_uri = f"/cards/search?q={name}&dir={dir}&page={page}"
        cache = repo.get_cache(method_uri)
        cached_cards = repo.search_cards(cache.id)
        if cached_cards is None or len(cached_cards) < 1:
            if rate_repo.check_rate_limit("scryfall", max_count=50, duration=1):
                resp = requests.get(f"{API_BASE_URI}{method_uri}", 
                                    headers={"user-agent": USER_AGENT, 
                                                "Accept": ACCEPTS})
                if resp.ok:
                    cached_cards = repo.cache_search_card_results(id, resp.json()["data"])
        return [c.dto() for c in cached_cards]