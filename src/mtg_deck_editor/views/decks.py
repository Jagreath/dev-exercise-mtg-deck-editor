from flask import (
    abort,
    g,
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from mtg_deck_editor.domain.models import (User, ValidationError)
from mtg_deck_editor.infrastructure.repos import DeckRepository
from mtg_deck_editor.util.parsing import parse_moxfield_string
from mtg_deck_editor.services.scryfall import ScryfallApi
from mtg_deck_editor.views.auth import authenticated

bp = Blueprint('decks', __name__)

scryfall_api = ScryfallApi()

@bp.route("/decks")
def decks():
    repo = DeckRepository()
    return render_template("decks/decks.html", decks=repo.get_all())

@bp.route("/decks/new")
@authenticated
def new_deck():
    current_user: User = g.user
    deck = current_user.add_deck("Lorem Ipsum")
    DeckRepository().save()
    return redirect(url_for("decks/decks.edit_deck", uuid=deck.uuid))

@bp.route("/decks/<uuid>")
def deck(uuid: str):
    repo = DeckRepository()
    return render_template("decks/view_deck.html", deck=repo.get(uuid))

@bp.route("/decks/<uuid>/edit")
@authenticated
def edit_deck(uuid: str):
    repo = DeckRepository()
    return render_template("decks/edit_deck.html", deck=repo.get(uuid))

@bp.post("/decks/<uuid>/save")
@authenticated
def save_deck(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)

    try:
        deck.name = request.form["name"]
        deck.description = request.form["description"]
    except ValidationError as e:
        return e.message, 400
    
    repo.save()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
@authenticated
def delete_deck(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    repo.delete(deck)
    repo.save()
    return redirect(url_for("decks.decks"))

@bp.post("/decks/<uuid>/add-card")
@authenticated
def add_card(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    
    try:
        card = deck.add_card(request.form["name"], 
                            int(request.form["quantity"]), 
                            request.form["set_code"],
                            request.form["collector_number"], 
                            request.form["mana_cost"],
                            request.form["mana_value"],
                            request.form["card_type"])
    except ValidationError as e:
        return e.message, 400
    
    repo.save()
    return { id : card.id }

@bp.post("/decks/<uuid>/remove-card")
@authenticated
def remove_card(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    deck.remove_card(request.args["id"])
    repo.save()

    return {}

@bp.post("/decks/<uuid>/update-card")
@authenticated
def update_card(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    card = next(c for c in deck.cards if c.id == int(request.args["id"]))
    if card is not None:
        if "quantity" in request.args:
            card.quantity = int(request.args["quantity"])
        if "set_code" in request.args:
            card.set_code = request.args["set_code"]
            card.collector_number = request.args["collector_number"]

    repo.save()

    return {}


