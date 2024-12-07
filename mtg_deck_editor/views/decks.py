from flask import (
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from .. import db
from ..models.decks import (
    Deck,
    Card
)
from ..models.sets import SetCard

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
    cards = db.session.execute(deck.cards.select()).scalars()
    return render_template("view_deck.html", deck=deck, cards=cards)

@bp.route("/decks/<uuid>/edit")
def edit_deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    cards = db.session.execute(deck.cards.select()).scalars()
    return render_template("edit_deck.html", deck=deck, cards=cards)

@bp.post("/decks/<uuid>/save")
def save_deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    db.session.add(deck)
    deck.name = request.form.get("name")
    deck.description = request.form.get("description")    
    #TODO update cards
    # deck.cards = parse_moxfield_decklist(request.form.get("cards"))

    db.session.commit()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
def delete_deck(uuid: str):
    deck = db.get_or_404(Deck, uuid)
    db.session.delete(deck)
    db.session.commit()
    return redirect(url_for("decks.decks"))

from re import compile as re_compile
_moxfield_decklist_pattern = re_compile(r"(\s*(?P<quantity>\d+)\s*)?(?P<name>[\d\w\s\-\,\'\/]+)(\((?P<set_code>[\d\w]{3,4})\)\s*)?((?P<collector_number>[\d\w\-★]{1,7})\s*)?.*")

def parse_moxfield_decklist(decklist: str) -> list[Card]:
    """
    Parse a string and find cards that exist.
    String format looks something like: 
    "4 this is a card name (SET) NUMBER"

    The set and number may be omitted.
    """
    cards = []
    if decklist is not None:
        
        for row in decklist.strip().splitlines():
            match = _moxfield_decklist_pattern.match(row)
            if match:
                params = {
                    "name": ""
                }
                if match.group("name"):
                    params["name"] = match.group("name").strip().title()
                if match.group("set_code"):
                    params["setCode"] = match.group("set_code").strip().upper()
                if match.group("collector_number"):
                    params["number"] = match.group("collector_number").strip().upper()

                set_card = db.session.execute(db.select(SetCard).filter_by(**params)).scalar()
                if set_card:
                    card = Card()
                    card.uuid = set_card.uuid
                    card.name = set_card.name
                    card.set_code = set_card.setCode
                    card.collector_number = set_card.number
                    card.quantity = int(match.group("quantity").strip()) if match.group("quantity") else 1
                    cards.append(card)
    return cards