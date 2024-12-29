from dataclasses import dataclass


@dataclass
class CardDto:
    id: str
    oracle_id: str
    cmc: int
    name: str
    mana_cost: str
    set: str
    collector_number: str