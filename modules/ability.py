from modules.bults import BaseAbility, \
    ActiveAbilityType, BoostType, ValueType, DamageType, Crit


class Ability(BaseAbility):
    def __init__(self, name: str, description: str = ""):
        self.__name = name
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description


class PassiveAbility(Ability):
    pass


class BoostAbility(PassiveAbility):
    def __init__(self, kind: BoostType, name: str, description: str):
        super().__init__(name=name, description=description)
        self.__kind = kind

    @property
    def kind(self):
        return self.__kind


class ActiveBoostAbility(BoostAbility):
    pass


class PassiveBoostAbility(BoostAbility):
    def __init__(self, kind: BoostType, name: str, description: str, enabled=False):
        super().__init__(kind=kind, name=name, description=description)
        self.enabled = enabled


class HealthBoost(PassiveBoostAbility):
    def __init__(self, name: str, description: str, value: dict = None, enabled=False):
        kind = BoostType.health
        if value is None:
            value = {ValueType.row: 0, ValueType.percent_M: 0}
        self.__value = value
        super().__init__(kind=kind, name=name, description=description, enabled=enabled)

    def get(self, value_type: ValueType):
        return self.__value.get(value_type, 0)


class ResistanceBoost(PassiveBoostAbility):
    def __init__(self, name: str, description: str, value: dict = None, enabled=False):
        kind = BoostType.resistance
        super().__init__(kind=kind, name=name, description=description, enabled=enabled)
        if value is None:
            value = {DamageType.fire: 0, DamageType.freeze: 0, DamageType.lightning: 0,
                     DamageType.physic: 0, DamageType.moral: 0}
        self.__value = value

    def get(self, damage_type: DamageType):
        return self.__value.get(damage_type, 0)


class ExperienceBoost(PassiveBoostAbility):
    def __init__(self, name: str, description: str, exp_mult: float):
        kind = BoostType.experience
        super().__init__(kind=kind, name=name, description=description)
        self.__exp_mult = exp_mult

    @property
    def exp_mult(self):
        return self.__exp_mult


class DamageBoost(ActiveBoostAbility):
    def __init__(self, name: str, description: str, dmg_value: dict = None, crit_value: dict = None):
        kind = BoostType.damage
        super().__init__(kind=kind, name=name, description=description)
        if dmg_value is None:
            dmg_value = {DamageType.fire: {ValueType.row: 0, ValueType.percent_M: 0},
                         DamageType.freeze: {ValueType.row: 0, ValueType.percent_M: 0},
                         DamageType.lightning: {ValueType.row: 0, ValueType.percent_M: 0},
                         DamageType.physic: {ValueType.row: 0, ValueType.percent_M: 0},
                         DamageType.moral: {ValueType.row: 0, ValueType.percent_M: 0},
                         DamageType.pure: {ValueType.row: 0, ValueType.percent_M: 0}}
        if crit_value is None:
            crit_value = {Crit.chance: 0, Crit.value: 0}
        self.__dmg_value = dmg_value
        self.__crit_value = crit_value

    def get_damage(self, damage_type: DamageType, value_type: ValueType = None):
        if value_type is None:
            return self.__dmg_value.get(damage_type, {ValueType.row: 0, ValueType.percent_M: 0})
        return self.__dmg_value.get(
            damage_type, {ValueType.row: 0, ValueType.percent_M: 0}).get(value_type, 0)

    def get_crit(self, key: Crit):
        return self.__crit_value.get(key, 0)


class HealBoost(ActiveBoostAbility):
    def __init__(self, name: str, description: str, heal_value: dict = None, crit_value: dict = None):
        kind = BoostType.heal
        super().__init__(kind=kind, name=name, description=description)
        if heal_value is None:
            heal_value = {ValueType.row: 0, ValueType.percent_M: 0}
        if crit_value is None:
            crit_value = {Crit.chance: 0, Crit.value: 0}
        self.__heal_value = heal_value
        self.__crit_value = crit_value

    def get_heal(self, value_type: ValueType):
        return self.__heal_value.get(value_type, 0)

    def get_crit(self, key: Crit):
        return self.__crit_value.get(key, 0)


class ActiveAbility(Ability):
    def __init__(self, kind: ActiveAbilityType, name: str, description: str = ""):
        super().__init__(name=name, description=description)
        self.__kind = kind

    @property
    def kind(self):
        return self.__kind

    def activate(self, sender, target):
        pass
