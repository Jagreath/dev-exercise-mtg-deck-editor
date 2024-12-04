from datetime import datetime
import sqlite3 as sql

from mtg_deck_editor.config import APP_CONFIG
from .models import (
    Deck, 
    DeckCard, 
    AtomicCard
)
    
class AtomicDb:
    SELECT_SETS = """   select  code as set_code,
                                name as set_name
                        from    sets """
    SELECT_CARDS = """  select  uuid,
                                name as card_name,
                                setCode as set_code,
                                number as collector_number
                        from    cards """

    def __init__(self, connection_str):
        self._connection = None
        self._connection_str = connection_str
    
    def connect(self):
        if self._connection is None:
            self._connection = sql.connect(self._connection_str, autocommit=True)
            self._connection.row_factory = sql.Row
    
    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def create_indicies(self):
        cursor = self._connection.cursor()
        cursor.execute("create index if not exists sets_code_idx on sets (code)")
        cursor.execute("create index if not exists cards_uuid_idx on cards (uuid)")
        cursor.execute("create index if not exists cards_name_idx on cards (name)")
        cursor.execute("create index if not exists cards_name_setcode_idx on cards (name, setCode)")
        cursor.execute("create index if not exists cards_name_setcode_number_idx on cards (name, setCode, number)")
        cursor.close()

    def get_cards_by_name_set_number(self, cards: list[AtomicCard]) -> AtomicCard:
        where_sql = f" where ({") or (".join(["lower(name) = ? " + ("and setCode = ?" if _.set_code else "") + ("and number = ?" if _.collector_number else "") for _ in cards])})"
        params = []
        for card in cards:
            params.append(card.name.lower())
            if card.set_code:
                params.append(card.set_code)
            if card.collector_number:
                params.append(card.collector_number)
        cursor = self._connection.execute(AtomicDb.SELECT_CARDS + where_sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return [AtomicCard(**r) for r in rows]
  
sql.register_adapter(datetime, lambda val: int(val.timestamp()))
sql.register_converter("date", lambda val: datetime.fromtimestamp(int(val)))

class DecksDb():
    def __init__(self, connection_str, atomic_connection_str):
        self._connection = None
        self._connection_str = connection_str
        self._atomic_connection_str = atomic_connection_str

    def connect(self):
        if self._connection is None:
            self._connection = sql.connect(self._connection_str, autocommit=True, detect_types=sql.PARSE_DECLTYPES)
            self._connection.row_factory = sql.Row
            cursor = self._connection.cursor()
            cursor.execute("attach database ? as atomic", [self._atomic_connection_str])
            cursor.close()

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def rebuild(self):
        cursor = self._connection.cursor()
        cursor.execute("drop table if exists main.cards")
        cursor.execute("""create table if not exists main.cards( deck_id INTEGER not null,
                                                            uuid TEXT not null,
                                                            quantity INTEGER not null)""")
        cursor.execute("drop table if exists main.decks")
        cursor.execute("""create table if not exists main.decks( id INTEGER PRIMARY KEY,
                                                            name TEXT not null,
                                                            description TEXT,
                                                            format TEXT not null,
                                                            created date not null,
                                                            changed date not null)""")
        cursor.close()

    def get_decks(self) -> list[Deck]:
        sql_str = """   select      id,
                                    name,
                                    description,
                                    format,
                                    created,
                                    changed
                        from        main.decks
                        order by    main.decks.name"""

        cursor = self._connection.execute(sql_str)
        rows = cursor.fetchall()
        cursor.close()
        return [Deck(**r) for r in rows]

    def get_deck_by_deck_id(self, id: int) -> Deck:
        select_deck_sql = """   select      main.decks.id,
                                            main.decks.name,
                                            main.decks.description,
                                            main.decks.format,
                                            main.decks.created,
                                            main.decks.changed
                                from        main.decks
                                where       main.decks.id = ?"""

        cursor = self._connection.execute(select_deck_sql, [id])
        row = cursor.fetchone()
        cursor.close()
        if row is not None:
            deck = Deck(**row)
            deck.cards = self._get_cards_by_deck_id(id)
            return deck
        return None

    def insert_deck(self, deck: Deck) -> Deck:
        insert_sql = """insert into main.decks   (   name, 
                                                description, 
                                                format, 
                                                changed, 
                                                created)
                        values              (?, ?, ?, ?, ?)
                        returning           id, name, description, format, changed, created"""
        cursor = self._connection.execute(insert_sql, [deck.name, deck.description, deck.format, deck.changed, deck.created])
        row = cursor.fetchone()
        cursor.close()
        return Deck(**row) if row is not None else None
    
    def delete_deck(self, id: int):
        self._delete_cards_by_deck_id(id)

        delete_sql = """    delete from main.decks 
                            where       id = ?
                            returning   id, name, description, format, changed, created"""
        cursor = self._connection.execute(delete_sql, [id])
        row = cursor.fetchone()
        cursor.close()

    def update_deck(self, deck: Deck):
        update_deck_sql = """   update  main.decks 
                                set     name = ?,
                                        description = ?,
                                        format = ?,
                                        changed = ?
                                where   id = ?
                                returning   id, name, description, format, changed, created"""
        cursor = self._connection.execute(update_deck_sql, [deck.name, deck.description, deck.format, deck.changed, deck.id])
        row = cursor.fetchone()
        cursor.close()
        if row is not None and len(deck.cards):
            self._delete_cards_by_deck_id(deck.id)
            self._insert_cards(deck.cards)

    def _get_cards_by_deck_id(self, deck_id: int):
        select_cards_sql = """  select      main.cards.deck_id,
                                            main.cards.uuid,
                                            main.cards.quantity,
                                            atomic.cards.name,
                                            atomic.cards.setCode as set_code,
                                            atomic.cards.number as collector_number
                                from        main.cards
                                join        atomic.cards
                                on          main.cards.uuid = atomic.cards.uuid
                                where       main.cards.deck_id = ?"""
        
        cursor = self._connection.execute(select_cards_sql, [deck_id])
        rows = cursor.fetchall()
        cursor.close()
        return [DeckCard(**row) for row in rows]

    def _delete_cards_by_deck_id(self, deck_id: int):
        delete_cards_sql = """  delete from main.cards 
                                where   deck_id = ?
                                returning deck_id, uuid, quantity"""
        cursor = self._connection.execute(delete_cards_sql, [deck_id])
        cursor.close()

    def _insert_cards(self, cards: list[DeckCard]):
        insert_cards_sql = """  insert into main.cards  (   deck_id, 
                                                            uuid,
                                                            quantity)
                                select                      ? as deck_id,
                                                            atomic.cards.uuid as uuid,
                                                            ? as quantity
                                from                        atomic.cards
                                where                       atomic.cards.name = ? """
        if cards and len(cards):
            for card in cards:
                params = [card.deck_id, card.quantity, card.name]
                i_sql = insert_cards_sql
                if card.set_code:
                    i_sql += " and atomic.cards.setCode = ? "
                    params.append(card.set_code)
                if card.collector_number:
                    i_sql += " and atomic.cards.number = ? "
                    params.append(card.collector_number)
                i_sql += " limit 1"
                cursor = self._connection.execute(i_sql, params)
                cursor.close()
  