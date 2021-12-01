from modules.item import AbilityItem
from modules.abilities.passive_boost import Stamina
from modules.bults import Slot


class Helmet(AbilityItem):
    def __init__(self, name: str, description: str, price: float,
                 abilities: list, req_level: int):
        super().__init__(name=name, description=description, price=price,
                         abilities=abilities, req_level=req_level, req_slot=Slot.head)


