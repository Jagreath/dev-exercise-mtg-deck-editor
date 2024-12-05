from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    abort,
    request,
    g
)
from flask_sqlalchemy import SQLAlchemy
from .config import APP_CONFIG

db = SQLAlchemy()

def create_app(config_obj=APP_CONFIG) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG)

    db.init_app(app)

    @app.route("/")
    @app.route("/decks")
    def decks():
        decks = db.session.execute(db.select(Deck).order_by(Deck.name)).scalars()
        return render_template("decks.html.jinja", decks=decks)

    @app.route("/decks/new")
    def new_deck():
        deck = Deck(
            name="Placeholder Name for a Deck",
            description="lorem ipsum, things of that nature")
        db.session.add(deck)
        db.session.commit()
        return redirect(url_for("edit_deck", uuid=deck.uuid))

    @app.route("/decks/<uuid>")
    def deck(uuid: str):
        deck = db.get_or_404(Deck, uuid)
        cards = db.session.execute(deck.cards.select()).scalars()
        return render_template("view_deck.html.jinja", deck=deck, cards=cards)

    @app.route("/decks/<uuid>/edit")
    def edit_deck(uuid: str):
        deck = db.get_or_404(Deck, uuid)
        cards = db.session.execute(deck.cards.select()).scalars()
        return render_template("edit_deck.html.jinja", deck=deck, cards=cards)

    @app.post("/decks/<uuid>/save")
    def save_deck(uuid: str):
        deck = db.get_or_404(Deck, uuid)
        db.session.add(deck)
        deck.name = request.form.get("name")
        deck.description = request.form.get("description")
        decklist = request.form.get("cards")
        if decklist is not None:
            deck.cards.delete()
            deck.parse_moxfield_decklist(decklist)
        db.session.commit()
        return redirect(url_for("deck", uuid=uuid))

    @app.route("/decks/<uuid>/delete")
    def delete_deck(uuid: str):
        deck = db.get_or_404(Deck, uuid)
        db.session.delete(deck)
        db.session.commit()
        return redirect(url_for("decks"))

    @app.teardown_appcontext
    def close_session(exception):
        db.session.remove()

    return app

from .models import (
    Deck,
    Card,
    Set,
    SetCard
)