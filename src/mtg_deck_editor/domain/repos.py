from mtg_deck_editor.domain.models import Deck, User

class BaseUserRepository:
    def get_by_uuid(self, uuid: str) -> User:
        pass

    def get_by_name(self, name: str) -> User:
        pass

    def get_all(self) -> list[User]:
        pass

    def add(self, user: User):
        pass

    def save(self, user: User):
        pass

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