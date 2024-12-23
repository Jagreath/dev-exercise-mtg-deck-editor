from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mtg_deck_editor.config import APP_CONFIG
from mtg_deck_editor.infra import maps

db = SQLAlchemy()

def create_app(config_obj=APP_CONFIG) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_obj)

    maps.create_all(db.metadata)
    db.init_app(app)

    from .views import decks
    app.register_blueprint(decks.bp)

    @app.teardown_appcontext
    def close_session(exception):
        db.session.remove()

    return app