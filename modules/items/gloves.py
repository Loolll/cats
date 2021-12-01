from modules.abilities.active_damage import Burn
from modules.abilities.passive_boost import PhysicResistance
from modules.bults import Slot
from modules.item import AbilityItem


class Gloves(AbilityItem):
    def __init__(self, name: str, description: str, price: float, abilities: list,
                 req_level: 1):
        super().__init__(name=name, description=description, price=price, abilities=abilities,
                         req_level=req_level, req_slot=Slot.gloves)


class Gloves1(Gloves):
    def __init__(self):
        super().__init__('gloves', 'xxxgloves', 33333, [Burn(100, 200)], 1)


class Gloves2(Gloves):
    def __init__(self):
        super().__init__('gloves', 'XXXgloves', 500, [PhysicResistance(1)], 1)
