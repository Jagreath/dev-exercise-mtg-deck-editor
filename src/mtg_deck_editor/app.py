from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mtg_deck_editor.infra import maps
from config import APP_CONFIG

db = SQLAlchemy()

def create_app(config_obj=APP_CONFIG) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_obj)

    maps.create_all(db.metadata)
    db.init_app(app)

    from .views.home import bp as home_bp
    app.register_blueprint(home_bp)

    from .views.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp)

    from .views.users import bp as users_bp
    app.register_blueprint(users_bp)

    from .views.decks import bp as decks_bp
    app.register_blueprint(decks_bp)

    @app.teardown_appcontext
    def close_session(exception):
        db.session.remove()

    return app