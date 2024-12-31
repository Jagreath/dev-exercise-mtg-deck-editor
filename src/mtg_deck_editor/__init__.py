from flask import Flask
from config import APP_CONFIG

def create_app(config_obj=APP_CONFIG) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_obj)

    from mtg_deck_editor.infrastructure import db, maps, events
    maps.create_all(db)
    events.add_events()
    db.init_app(app)

    from .views.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from .views.home import bp as home_bp
    app.register_blueprint(home_bp)

    from .views.auth import bp as accounts_bp
    app.register_blueprint(accounts_bp)

    from .views.users import bp as users_bp
    app.register_blueprint(users_bp)

    from .views.decks import bp as decks_bp
    app.register_blueprint(decks_bp)

    @app.teardown_appcontext
    def close_session(exception):
        db.session.remove()

    return app