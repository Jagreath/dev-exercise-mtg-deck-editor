from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import registry, relationship
from sqlalchemy.schema import MetaData
from mtg_deck_editor.domain.decks import Deck, Card
from mtg_deck_editor.services.models import CachedCard, RateLimit, ScryfallCache

def create_decks(registry: registry):
    decks_table = Table(
        "decks",
        registry.metadata,
        Column("uuid", String(36), primary_key=True),
        Column("name", String(50), nullable=False),
        Column("description", String()),
        Column("created", DateTime, nullable=False),
        Column("modified", DateTime, nullable=False)
    )
    registry.map_imperatively(
        Deck, 
        decks_table,
        properties={
            "cards": relationship(Card, back_populates="deck", cascade="all, delete-orphan")
        })
    
def create_cards(registry: registry):
    cards_table = Table(
        "cards",
        registry.metadata,
        Column("uuid", String(36), primary_key=True),
        Column("deck_uuid", String(36), ForeignKey("decks.uuid"), primary_key=True, index=True),
        Column("quantity", Integer, nullable=False),
        Column("name", String(255), nullable=False),
        Column("set_code", String(12), nullable=False),
        Column("collector_number", String(12), nullable=False),
        Column("mana_cost", String(32), nullable=True),
        Column("mana_value", Integer, nullable=True),
        Column("created", DateTime, nullable=False),
        Column("modified", DateTime, nullable=False)
    )
    registry.map_imperatively(
        Card,
        cards_table,
        properties={
            "deck": relationship(Deck, back_populates="cards")
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
        "cached_cards",
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
            "cache": relationship(back_populates="cached_cards")
        }
    )

def create_all(metadata: MetaData):
    mapper_registry = registry(metadata=metadata)
    create_decks(mapper_registry)
    create_cards(mapper_registry)
    create_rate_limit(mapper_registry)
    create_scryfall_cache(mapper_registry)
    create_cached_card(mapper_registry)

    



