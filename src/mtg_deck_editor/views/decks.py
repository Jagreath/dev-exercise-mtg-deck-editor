from flask import (
    abort,
    g,
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from mtg_deck_editor.domain.models import (Deck, User, ValidationError)
from mtg_deck_editor.infrastructure.repos import DeckRepository
from mtg_deck_editor.util.parsing import parse_moxfield_string
from mtg_deck_editor.services.scryfall import ScryfallApi
from mtg_deck_editor.views.auth import authorized

bp = Blueprint('decks', __name__)

scryfall_api = ScryfallApi()

@bp.route("/decks")
def decks():
    repo = DeckRepository()
    return render_template("decks/decks.html", decks=repo.get_all())

@bp.route("/decks/new")
@authorized
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
@authorized
def edit_deck(uuid: str):
    repo = DeckRepository()
    return render_template("decks/edit_deck.html", deck=repo.get(uuid))

@bp.post("/decks/<uuid>/save")
@authorized
def save_deck(uuid: str):

    repo = DeckRepository()
    deck = repo.get(uuid)
    deck.name = request.form["name"]
    deck.description = request.form["description"]
    
    deck.cards.clear()
    for card_string in request.form.get("cards", "").strip().splitlines():
        name, set_code, collector_number, quantity = parse_moxfield_string()
        card_dto = scryfall_api.get_card(set_code, collector_number)
        if card_dto is not None:
            deck.add_card(card_dto.id,
                          card_dto.name,
                          card_dto.set,
                          card_dto.collector_number,
                          card_dto.mana_cost,
                          card_dto.cmc,
                          quantity)

    repo.save()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
def delete_deck(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    repo.delete(deck)
    repo.save()
    return redirect(url_for("decks.decks"))

@bp.post("/decks/<uuid>/cards/add")
@authorized
def add_card(uuid: str):
    repo = DeckRepository()
    deck = repo.get(uuid)
    
    card = deck.add_card(request.form["name"], 
                        int(request.form["quantity"]), 
                        request.form["set_code"],
                        request.form["collector_number"], 
                        request.form["mana_cost"],
                        request.form["mana_value"],
                        request.form["card_type"])
    repo.save()
    return { id : card.id }

@bp.post("/decks/<uuid>/cards/<id>/update")
@authorized
def update_card(uuid: str, id: int):
    repo = DeckRepository()
    deck = repo.get(uuid)

    card = next(c for c in deck.cards if c.id == id)
    card.quantity = int(request.form["quantity"])
    card.set_code = request.form["set_code"]
    card.collector_number = request.form["collector_number"]

    repo.save()
    return {}

@bp.post("/decks/<uuid>/cards/<id>/delete")
@authorized
def delete_card(uuid: str, id: int):
    repo = DeckRepository()
    deck = repo.get(uuid)
    deck.remove_card(id)
    repo.save()

    return {}


