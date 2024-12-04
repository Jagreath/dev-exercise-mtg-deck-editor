from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    abort,
    request,
    g
)
from markupsafe import escape
from mtg_deck_editor.config import APP_CONFIG
from mtg_deck_editor.sqlitedb import (
    DecksDb
)
from mtg_deck_editor.models import (
    Deck
)

app = Flask(__name__)

def _get_deckdb() -> DecksDb:
    db = getattr(g, '_deckdb', None)
    if db is None:
        db = g._deckdb = DecksDb(APP_CONFIG.DECKS_CONNECTION, APP_CONFIG.ATOMIC_CONNECTION)
        db.connect()
    return db

# @app.route("/")
# def index():
#     return redirect(url_for("decks"))

@app.route("/decks")
def decks():
    decks = _get_deckdb().get_decks()
    return render_template("decks.html.jinja", decks=decks)

@app.route("/decks/new")
def new_deck():
    deck = Deck(
        name="Placeholder Name for a Deck",
        description="lorem ipsum, things of that nature",
        format="Standard")
    deck = _get_deckdb().insert_deck(deck)
    return redirect(url_for("edit_deck", id=deck.id))

@app.route("/decks/<int:id>")
def deck(id: int):
    deck = _get_deckdb().get_deck_by_deck_id(id)
    if deck is not None:
        return render_template("view_deck.html.jinja", deck=deck)
    return abort(404)

@app.route("/decks/<int:id>/edit")
def edit_deck(id: int):
    deck = _get_deckdb().get_deck_by_deck_id(id)
    return render_template("edit_deck.html.jinja", deck=deck)

@app.post("/decks/<int:id>/save")
def save_deck(id: int):
    deck = _get_deckdb().get_deck_by_deck_id(id)
    deck.name = request.form.get("name")
    deck.description = request.form.get("description")
    deck.parse_and_replace_cards(request.form.get("cards"))
    _get_deckdb().update_deck(deck)
    return redirect(url_for("deck", id=id))

@app.route("/decks/<int:id>/delete")
def delete_deck(id: int):
    _get_deckdb().delete_deck(id)
    return redirect(url_for("decks"))

@app.teardown_appcontext
def close_connections(exception):
    deckdb = getattr(g, "_deckdb", None)
    if deckdb is not None:
        deckdb.close()

if __name__ == "__main__":
    app.run(debug=True)