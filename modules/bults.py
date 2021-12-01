import random
from enum import Enum


class DamageType(Enum):
    fire = "fire"
    freeze = "freeze"
    lightning = "lightning"
    moral = "moral"
    physic = "physic"
    pure = "pure"


class Crit(Enum):
    chance = "chance"
    value = "value"


class ReceivedValueType(Enum):
    low = "low"
    high = "high"
    calculated = "calculated"


class ValueType(Enum):
    row = "row"
    percent_T = "percent_T"  # in range(0,1)
    percent_M = "percent_M"  # in range(0,1)


class MsgType(Enum):
    hello = "hello"
    die = "die"
    deal_damage = "deal_damage"
    take_damage = "take_damage"
    restore = "restore"
    resurrect = "resurrect"


class BoostType(Enum):
    health = "health"
    resistance = "resistance"
    experience = "experience"
    damage = "damage"
    heal = "heal"


class Slot(Enum):
    inventory = "inventory"
    head = "head"
    hand_right = "hand_right"
    hand_left = "hand_left"
    ring = "ring"
    necklace = "necklace"
    body = "body"
    gloves = "gloves"
    legs = "legs"
    boots = "boots"


class ActiveAbilityType(Enum):
    attack = "attack"
    heal = "heal"


class Voice:
    def __init__(self, messages: dict = None):
        if messages is None:
            messages = {MsgType.hello: ["Hello, I'm yr big brother"],
                        MsgType.die: ["Goodbye Everyone ("],
                        MsgType.deal_damage: ["Get it!"],
                        MsgType.take_damage: ["((("],
                        MsgType.restore: ["hi-hi-hi"],
                        MsgType.resurrect: ["Ya snova jivu"]}
        self.__messages = messages

    def exists(self, key: MsgType):
        return key in self.__messages.keys()

    def speak(self, key: MsgType, default: list = ("")):
        return random.choice(self.__messages.get(key, default))

    def change_message(self, key: MsgType, value: list):
        self.__messages[key] = value



class BaseAnimal:
    pass


class BaseAbility:
    pass


class BaseItem:
    pass

class BasePlace:
    pass