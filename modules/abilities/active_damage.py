from modules.ability import ActiveAbility, ActiveAbilityType
from modules.features import Damage
from modules.bults import DamageType, ValueType


class DefaultAttack(ActiveAbility):
    def __init__(self, description: str, name: str, damage_low: dict, damage_high: dict,
                 critical_chance: float = 0, critical_value: float = 2):
        kind = ActiveAbilityType.attack
        super().__init__(kind=kind, name=name, description=description)
        self.__damage = Damage(damage_low, damage_high, critical_chance, critical_value)

    @property
    def damage(self):
        return self.__damage

    def activate(self, sender, target):
        sender.make_damage(self.__damage, target)


class Scratch(DefaultAttack):
    def __init__(self, low_physic_row_damage: float, high_physic_row_damage: float,
                 critical_chance: float = 0, critical_value: float = 2,
                 name: str = "Царапнуть"):
        damage_low = {DamageType.physic: {ValueType.row: low_physic_row_damage}}
        damage_high = {DamageType.physic: {ValueType.row: high_physic_row_damage}}
        description = f"Царапает врага, нанося ему " \
                      f"{low_physic_row_damage}-{high_physic_row_damage} физического урона.\n" \
                      f"Критический шанс {critical_chance*100}%.\n" \
                      f"Множитель {critical_value}"
        super().__init__(name=name, description=description,
                         damage_low=damage_low, damage_high=damage_high,
                         critical_chance=critical_chance, critical_value=critical_value)


class Burn(DefaultAttack):
    def __init__(self, low_fire_row_damage: float, high_fire_row_damage: float,
                 critical_chance: float = 0.3, critical_value: float = 2,
                 name: str = "Обжечь"):
        damage_low = {DamageType.fire: {ValueType.row: low_fire_row_damage}}
        damage_high = {DamageType.fire: {ValueType.row: high_fire_row_damage}}
        description = f"Обжигает врага, нанося ему {low_fire_row_damage}-{high_fire_row_damage}" \
                      f" урона огнем. " \
                      f"Критический шанс {critical_chance*100}%.\n" \
                      f"Множитель {critical_value}"

        super().__init__(name=name, description=description,
                         damage_low=damage_low, damage_high=damage_high,
                         critical_chance=critical_chance, critical_value=critical_value)

