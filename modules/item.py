from modules.animal import Fighter
from modules.bults import BaseItem, Slot
from modules.tools import deepcopy
from modules.exceptions import NotInInventoryError, CantWearError, NotEnoughSpaceException, UnexpectedSlotException, WrongItemError


class Item(BaseItem):
    def __init__(self, name: str, description: str, price: float):
        self.__name = name
        self.__description = description
        self.__price = price

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price


class AbilityItem(Item):
    def __init__(self, name: str, description: str, price: float,
                 abilities: list, req_level: int, req_slot: Slot):
        super().__init__(name=name, description=description, price=price)
        self.__abilities = deepcopy(abilities)
        self.__req_level = req_level
        self.__req_slot = req_slot

    @property
    def req_level(self):
        return self.__req_level

    @property
    def abilities(self):
        return self.__abilities

    @property
    def req_slot(self):
        return self.__req_slot


class Inventory:
    def __init__(self, owner: Fighter, max_size: int, backpack: set = None, slots: dict = None):
        if backpack is None:
            backpack = set()
        if slots is None:
            slots = {Slot.head: None, Slot.hand_left: None, Slot.hand_right: None,
                     Slot.ring: None, Slot.necklace: None, Slot.body: None,
                     Slot.gloves: None, Slot.legs: None, Slot.boots: None}
        self.__owner = owner
        self.__max_size = max_size
        self.__slots = slots
        self.__backpack = backpack

    @property
    def backpack(self):
        return self.__backpack.copy()

    @property
    def slots(self):
        return self.__slots.copy()

    @property
    def max_size(self):
        return self.__max_size

    @property
    def size(self):
        return len(self.__backpack)

    def can_wear(self, item: AbilityItem):
        if item.req_level <= self.__owner.level and item.req_slot in self.__slots:
            return True
        return False

    def is_slot_empty(self, slot: Slot):
        if self.__slots[slot]:
            return True
        return False

    @property
    def have_empty_space(self):
        return self.size < self.__max_size

    def add(self, item: Item):
        if not self.have_empty_space:
            raise NotEnoughSpaceException
        self.__backpack.add(item)

    def change(self, inventory_item: Item, new_item: Item):
        self.__backpack.remove(inventory_item)
        self.__backpack.add(new_item)

    def remove(self, item: Item):
        if item not in self.__backpack:
            raise NotInInventoryError
        self.__backpack.remove(item)

    def put_off(self, item: AbilityItem = None):
        if item is not None:
            if not self.have_empty_space:
                raise NotEnoughSpaceException
            if item.req_slot not in self.__slots:
                raise UnexpectedSlotException
            if self.__slots[item.req_slot] is not item:
                raise WrongItemError
            self.add(item)
            self.__slots[item.req_slot] = None

    def put_on(self, item: AbilityItem):
        if item not in self.__backpack:
            raise NotInInventoryError
        if not self.can_wear(item):
            raise CantWearError
        self.remove(item)
        try:
            self.put_off(self.__slots[item.req_slot])
            self.__slots[item.req_slot] = item
        except UnexpectedSlotException:
            self.add(item)

    def get_abilities(self, ability_type: type):
        result = []
        items = [item for item in self.__backpack
                 if isinstance(item, AbilityItem) and item.req_slot == Slot.inventory and
                 item.req_level <= self.__owner.level] + \
                [self.__slots[slot] for slot in self.__slots
                 if self.__slots[slot] is not None and isinstance(self.__slots[slot], AbilityItem)]
        for item in items:
            result += [ability for ability in item.abilities if isinstance(ability, ability_type)]
        return result

    def sell_item(self, item: Item):
        if item not in self.__backpack:
            raise NotInInventoryError
        self.remove(item)
        return item.price
