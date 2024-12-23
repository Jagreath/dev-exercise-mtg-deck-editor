from mtg_deck_editor.domain.decks import Deck

class DeckRepositoryFactory:
    def create(self) -> "BaseDeckRepository":
        return None

class BaseDeckRepository:
    def get(self, uuid: str) -> Deck:
        pass

    def get_all(self) -> list[Deck]:
        pass

    def add(self, deck: Deck):
        pass

    def delete(self, deck: Deck):
        pass

    def save(self, deck: Deck):
        pass