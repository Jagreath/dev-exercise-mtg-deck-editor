from mtg_deck_editor.config import APP_CONFIG
from mtg_deck_editor.sqlitedb import (
    DecksDb,
    AtomicDb
)

def main():
    atomic_db = AtomicDb(APP_CONFIG.ATOMIC_CONNECTION)
    atomic_db.connect()
    atomic_db.create_indicies()
    atomic_db.close()

    deck_db = DecksDb(APP_CONFIG.DECKS_CONNECTION, APP_CONFIG.ATOMIC_CONNECTION)
    deck_db.connect()
    deck_db.rebuild()
    deck_db.close()


        
if __name__ == "__main__":
    main()