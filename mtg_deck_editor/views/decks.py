from flask import (
    abort,
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from .. import db
from ..models.decks import Deck
from ..models.sets import SetCard
from ..parsing.moxfield import MoxfieldParser

bp = Blueprint('decks', __name__)

@bp.route("/decks")
def decks():
    decks = db.session.execute(db.select(Deck).order_by(Deck.name)).scalars()
    return render_template("decks.html", decks=decks)

@bp.route("/decks/new")
def new_deck():
    deck = Deck(
        name="Placeholder Name for a Deck",
        description="lorem ipsum, things of that nature")
    db.session.add(deck)
    db.session.commit()
    return redirect(url_for("decks.edit_deck", uuid=deck.uuid))

@bp.route("/decks/<uuid>")
def deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    return render_template("view_deck.html", deck=deck)

@bp.route("/decks/<uuid>/edit")
def edit_deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    return render_template("edit_deck.html", deck=deck)

@bp.post("/decks/<uuid>/save")
def save_deck(uuid: str, cardParser = MoxfieldParser):
    deck = db.get_or_404(Deck, uuid)

    if "name" not in request.form \
        or "description" not in request.form \
        or "cards" not in request.form:
            abort(400)

    deck.name = request.form.get("name")
    deck.description = request.form.get("description")    
    deck.cards.clear()

    cards = cardParser().parse_lines(request.form.get("cards"))
    card_uuids = set()
    for card in cards:
        set_card = None
        if card.set_code and card.collector_number:
            set_card = db.session.execute(db.select(SetCard) \
                                          .where(SetCard.setCode == card.set_code \
                                                 and SetCard.number == card.collector_number)).scalar()
        elif card.name:
            set_card = db.session.execute(db.select(SetCard) \
                                          .where(SetCard.name == card.name)).scalar()
        if set_card is not None and set_card.uuid not in card_uuids:
            card_uuids.add(set_card.uuid)
            card.uuid = set_card.uuid
            card.name = set_card.name
            card.set_code = set_card.setCode
            card.collector_number = set_card.number
            card.mana_cost = set_card.manaCost
            card.mana_value = set_card.manaValue
            deck.cards.append(card)

    db.session.commit()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
def delete_deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    db.session.delete(deck)
    db.session.commit()
    return redirect(url_for("decks.decks"))
