import mtg_deck_editor

if __name__ == "__main__":
    app = mtg_deck_editor.create_app()
    with app.app_context() as context:
        mtg_deck_editor.db.drop_all()
        mtg_deck_editor.db.create_all()