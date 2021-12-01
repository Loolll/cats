from modules.ability import HealthBoost, DamageBoost, ResistanceBoost
from modules.bults import ValueType, Crit, DamageType



class Stamina(HealthBoost):
    def __init__(self, row_health: float, name: str = "Stamina", enabled=False):
        description = f"Увеличивает кол-во максимального здоровья на {row_health}."
        super().__init__(name=name, description=description, enabled=enabled,
                         value={ValueType.row: row_health})


class CritBoost(DamageBoost):
    def __init__(self, crit_value: dict, name: str = "CritBoost"):
        description = f"Увеличивает критический шанс на {crit_value.get(Crit.chance)*100}% " \
                      f"и критический множитель на {crit_value.get(Crit.value)}."
        super().__init__(name=name, description=description, crit_value=crit_value)


class FireDamageBoost(DamageBoost):
    def __init__(self, row_fire_damage: float, name: str = "FireDamageBoost"):
        description = f"Увеличивает урон от огня на {row_fire_damage}."
        super().__init__(name=name, description=description, dmg_value={
            DamageType.fire: {ValueType.row: row_fire_damage}})


class PhysicResistance(ResistanceBoost):
    def __init__(self, value: float, name="ResistanceBoost"):
        description = f"Увеличивает сопротивление к физическому урону на {value*100}%."
        super().__init__(name=name, description=description, value={DamageType.physic: value})