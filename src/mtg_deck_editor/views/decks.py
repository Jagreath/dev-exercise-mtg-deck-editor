from flask import (
    abort,
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from mtg_deck_editor.models.decks import (Deck, Card)
from mtg_deck_editor.parsing.cards import (MoxfieldParser)
from mtg_deck_editor.services.scryfall import ScryfallApi

bp = Blueprint('decks', __name__)

@bp.route("/decks")
def decks():
    return render_template("decks.html", decks=Deck.get_all())

@bp.route("/decks/new")
def new_deck():
    deck = Deck.new()
    deck.save()
    return redirect(url_for("decks.edit_deck", uuid=deck.uuid))

@bp.route("/decks/<uuid>")
def deck(uuid: str):
    return render_template("view_deck.html", deck=Deck.get(uuid))

@bp.route("/decks/<uuid>/edit")
def edit_deck(uuid: str):
    return render_template("edit_deck.html", deck=Deck.get(uuid))

@bp.post("/decks/<uuid>/save")
def save_deck(uuid: str):
    # TODO: form validation
    if "name" not in request.form \
        or "description" not in request.form \
        or "cards" not in request.form:
            abort(400, "Missing")


    deck = Deck.get(uuid)
    deck.name = request.form.get("name")
    deck.description = request.form.get("description")    
    
    deck.cards.clear()
    for card_string in request.form.get("cards").strip().splitlines():
        card = MoxfieldParser().parse_string(card_string)
        scryfall_card = None

        if card.set_code and card.collector_number:
            scryfall_card = ScryfallApi().get_card(card.set_code, card.collector_number)
        elif card.name:
            cards = ScryfallApi().search_cards(card.name)
            if len(cards) > 0:
                scryfall_card = cards[0]
        if scryfall_card is not None:
            card.copy_scryfall_dto(scryfall_card)
            deck.add_card(card)

    deck.save()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
def delete_deck(uuid: str):
    deck = Deck.get(uuid)
    deck.delete()
    deck.save()
    return redirect(url_for("decks.decks"))
