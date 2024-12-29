from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import registry, relationship
from mtg_deck_editor.domain.models import Tag, User, Deck, Card
from mtg_deck_editor.services.models import CachedCard, RateLimit, ScryfallCache

def create_users(registry: registry):
    users_table = Table(
        "users",
        registry.metadata,
        Column("uuid", String(36), primary_key=True),
        Column("name", String(256), nullable=False, index=True),
        Column("hash", String(256), nullable=False),
        Column("created", DateTime, nullable=False),
        Column("modified", DateTime, nullable=False),
        Column("accessed", DateTime, nullable=False)
    )
    registry.map_imperatively(
        User,
        users_table,
        properties={
            "_decks": relationship(Deck, back_populates="user", cascade="all, delete-orphan")
        }
    )

def create_decks(registry: registry):
    decks_table = Table(
        "decks",
        registry.metadata,
        Column("uuid", String(36), primary_key=True),
        Column("user_uuid", String(36), ForeignKey("users.uuid")),
        Column("_name", String(50), nullable=False),
        Column("_description", String()),
        Column("created", DateTime, nullable=False),
        Column("modified", DateTime, nullable=False)
    )
    registry.map_imperatively(
        Deck, 
        decks_table,
        properties={
            "_user": relationship(User, back_populates="_decks"),
            "_cards": relationship(Card, back_populates="_deck", cascade="all, delete-orphan")
        })
    
def create_cards(registry: registry):
    cards_table = Table(
        "cards",
        registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("deck_uuid", String(36), ForeignKey("decks.uuid")),
        Column("_name", String(255), nullable=False),
        Column("_quantity", Integer, nullable=False),
        Column("_set_code", String(12), nullable=False),
        Column("_collector_number", String(12), nullable=False),
        Column("mana_cost", String(32)),
        Column("mana_value", Integer),
        Column("card_type", String(32)),
        Column("created", DateTime, nullable=False),
        Column("modified", DateTime, nullable=False)
    )
    registry.map_imperatively(
        Card,
        cards_table,
        properties={
            "_deck": relationship(Deck, back_populates="_cards"),
            "_tags": relationship(Tag, back_populates="_card", cascade="all, delete-orphan")
        }
    )

def create_tags(registry: registry):
    tags_table = Table(
        "tags",
        registry.metadata,
        Column("name", String(32), primary_key=True),
        Column("deck_uuid", String(36), ForeignKey("decks.uuid"), primary_key=True),
        Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True)
    )
    registry.map_imperatively(
        Tag,
        tags_table,
        properties={
            "_card": relationship(Card, back_populates="_tags"),
        }
    )

def create_rate_limit(registry: registry):
    rate_limit_table = Table(
        "rate_limits",
        registry.metadata,
        Column("service", String(255), primary_key=True),
        Column("count", Integer, nullable=False, default=0),
        Column("limit_window", DateTime, nullable=True)
    )
    registry.map_imperatively(
        RateLimit, 
        rate_limit_table)
    
def create_scryfall_cache(registry: registry):
    scryfall_cache_table = Table(
        "scryfall_caches",
        registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("method_uri", String(255), nullable=False),
        Column("expiry", DateTime, nullable=True)
    )
    registry.map_imperatively(
        ScryfallCache,
        scryfall_cache_table,
        properties={
            "cached_cards": relationship(CachedCard,cascade="all, delete-orphan", passive_deletes=True, lazy="write_only")
        }
    )

def create_cached_card(registry: registry):
    cached_card_table = Table(
        "scryfall_cached_cards",
        registry.metadata,
        Column("cache_id", Integer, ForeignKey("scryfall_caches.id"), primary_key=True),
        Column("id", String(36), primary_key=True),
        Column("name", String(255)),
        Column("mana_cost", String(255)),
        Column("set", String(255)),
        Column("collector_number", String(255)),
        Column("cmc", String(255))
    )
    registry.map_imperatively(
        CachedCard,
        cached_card_table,
        properties={
            "sf_cache": relationship(ScryfallCache, back_populates="cached_cards")
        }
    )

def create_all(db: SQLAlchemy):
    mapper_registry = registry(metadata=db.metadata)
    create_users(mapper_registry)
    create_decks(mapper_registry)
    create_cards(mapper_registry)
    create_tags(mapper_registry)
    create_rate_limit(mapper_registry)
    create_scryfall_cache(mapper_registry)
    create_cached_card(mapper_registry)

    



