from mtg_deck_editor.app import create_app, db

if __name__ == "__main__":
    app = create_app()
    with app.app_context() as context:
        db.drop_all()
        db.create_all()