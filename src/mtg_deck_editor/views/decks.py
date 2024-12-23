from flask import (
    abort,
    url_for,
    render_template,
    redirect,
    request,
    Blueprint
)
from mtg_deck_editor.infra.repos import ContextDeckRepositoryFactory, ContextRateLimitRepositoryFactory, ContextScryfallCacheRepositoryFactory
from mtg_deck_editor.domain.decks import (Deck)
from mtg_deck_editor.parsing.cards import (MoxfieldParser)
from mtg_deck_editor.services.scryfall import ScryfallApi

bp = Blueprint('decks', __name__)

scryfall_api = ScryfallApi(ContextScryfallCacheRepositoryFactory(), ContextRateLimitRepositoryFactory())
moxfield_parser = MoxfieldParser()
deck_repo_factory = ContextDeckRepositoryFactory()

@bp.route("/decks")
def decks():
    repo = deck_repo_factory.create()
    return render_template("decks.html", decks=repo.get_all())

@bp.route("/decks/new")
def new_deck():
    deck = Deck()
    repo = deck_repo_factory.create()
    repo.add(deck)
    repo.save()
    return redirect(url_for("decks.edit_deck", uuid=deck.uuid))

@bp.route("/decks/<uuid>")
def deck(uuid: str):
    repo = deck_repo_factory.create()
    return render_template("view_deck.html", deck=repo.get(uuid))

@bp.route("/decks/<uuid>/edit")
def edit_deck(uuid: str):
    repo = deck_repo_factory.create()
    return render_template("edit_deck.html", deck=repo.get(uuid))

@bp.post("/decks/<uuid>/save")
def save_deck(uuid: str):
    # TODO: form validation
    if "name" not in request.form \
        or "description" not in request.form \
        or "cards" not in request.form:
            abort(400, "Missing")

    repo = deck_repo_factory.create()
    deck = repo.get(uuid)
    deck.name = request.form.get("name")
    deck.description = request.form.get("description")    
    
    deck.cards.clear()
    for card_string in request.form.get("cards").strip().splitlines():
        card = moxfield_parser.parse_string(card_string)
        scryfall_card = None

        if card.set_code and card.collector_number:
            scryfall_card = scryfall_api.get_card(card.set_code, card.collector_number)
        elif card.name:
            cards = scryfall_api.search_cards(card.name)
            if len(cards) > 0:
                scryfall_card = cards[0]
        if scryfall_card is not None:
            card.copy_scryfall_dto(scryfall_card)
            deck.add_card(card)

    repo.save()
    return redirect(url_for("decks.deck", uuid=uuid))

@bp.route("/decks/<uuid>/delete")
def delete_deck(uuid: str):
    repo = deck_repo_factory.create()
    deck = repo.get(uuid)
    repo.delete(deck)
    repo.save()
    return redirect(url_for("decks.decks"))
