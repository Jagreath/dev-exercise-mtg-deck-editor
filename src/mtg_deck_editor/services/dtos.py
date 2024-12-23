class CardDto:
    def __init__(self, 
                 id: str = "", 
                 cmc: int = 0, 
                 name: str = "", 
                 mana_cost: str = "", 
                 set: str = "", 
                 collector_number: str = ""):
        self.id = id
        self.cmc = cmc
        self.name = name
        self.mana_cost = mana_cost
        self.set = set
        self.collector_number = collector_number