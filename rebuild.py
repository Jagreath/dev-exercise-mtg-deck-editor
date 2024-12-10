from mtg_deck_editor.config import APP_CONFIG
from mtg_deck_editor import create_app, db

if __name__ == "__main__":
    app = create_app()
    with app.app_context() as context:
        db.drop_all(bind_key="DECKS")
        db.create_all(bind_key="DECKS")
