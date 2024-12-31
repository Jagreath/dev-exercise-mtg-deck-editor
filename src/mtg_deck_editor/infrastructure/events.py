from datetime import datetime, timezone
from sqlalchemy import event

from mtg_deck_editor.domain.models import User, Deck, Card

def user_on_insert_listener(m, c, target: User):
    utcnow = datetime.now(timezone.utc)
    target.created = utcnow
    target.modified = utcnow

def user_on_update_listener(m, c, target: User):
    target.modified = datetime.now(timezone.utc)

def deck_on_insert_listener(m, c, target: Card):
    utcnow = datetime.now(timezone.utc)
    target.created = utcnow
    target.modified = utcnow

def deck_on_update_listener(m, c, target: Deck):
    target.modified = datetime.now(timezone.utc)

def card_on_insert_listener(m, c, target: Card):
    utcnow = datetime.now(timezone.utc)
    target.created = utcnow
    target.modified = utcnow
    
def card_on_update_listener(m, c, target: Card):
    target.modified = datetime.now(timezone.utc)

def add_events():
    
    event.listen(User, "before_insert", user_on_insert_listener)
    event.listen(User, "before_update", user_on_update_listener)
    event.listen(Deck, "before_insert", deck_on_insert_listener)
    event.listen(Deck, "before_update", deck_on_update_listener)
    event.listen(Card, "before_insert", card_on_insert_listener)
    event.listen(Card, "before_update", card_on_update_listener)
    