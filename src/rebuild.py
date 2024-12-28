from mtg_deck_editor import create_app
from mtg_deck_editor.infrastructure import db

if __name__ == "__main__":
    app = create_app()
    with app.app_context() as context:
        db.drop_all()
        db.create_all()