from modules.ability import ResistanceBoost, HealthBoost, DamageBoost, HealBoost, ExperienceBoost
from modules.bults import DamageType, ValueType, ReceivedValueType, Crit
from modules.tools import number_between, calculate_crit


class Experience:
    """ exp_road - param means how much exp we need to have cur level.
        It's list with first and second values [0,1].
        exp >= 1 !!! """

    def __init__(self, max_level: int, exp: float = 1, exp_road: list = None, exp_mult: float = 1):
        self.__max_level = max_level
        if exp_road is None:
            exp_road = [0] + [2 ** i for i in range(0, max_level + 1)]
        self.__exp_road = exp_road
        self.__exp = exp
        self.__exp_mult = exp_mult

    @property
    def exp(self):
        return self.__exp

    @property
    def level(self):
        for lvl in range(1, self.__max_level + 1):
            need = self.__exp_road[lvl]
            if need > self.__exp:
                return lvl - 1
        return self.__max_level

    @property
    def max_level(self):
        return self.__max_level

    @property
    def for_next_level(self):
        if self.level != self.__max_level:
            return self.__exp_road[self.level + 1] - self.__exp
        return None

    def __change_row_exp(self, value: float):
        self.__exp = max(1, self.__exp + value)

    def add_exp(self, exp: float):
        self.__change_row_exp(exp * self.__exp_mult)

    def lost_exp(self, exp: float):
        self.__change_row_exp(-exp * self.__exp_mult)

    def activate_boost(self, boost: ExperienceBoost):
        if not boost.enabled:
            self.__exp_mult += boost.exp_mult
        boost.enabled = True

    def deactivate_boost(self, boost: ExperienceBoost):
        if boost.enabled:
            self.__exp_mult -= boost.exp_mult
        boost.enabled = False


class LeaderExperience(Experience):
    def __init__(self, exp:float):
        super().__init__(7, exp, [0,1,100,500,2000,5000,10000,20000], 1)

class Damage:
    def __init__(self, damage_low: dict = None, damage_high: dict = None,
                 critical_chance: float = 0,
                 critical_value: float = 2):
        if damage_low is None:
            damage_low = {DamageType.fire: {ValueType.row: 0,
                                            ValueType.percent_M: 0, ValueType.percent_T: 0},
                          DamageType.freeze: {ValueType.row: 0,
                                              ValueType.percent_M: 0, ValueType.percent_T: 0},
                          DamageType.lightning: {ValueType.row: 0,
                                                 ValueType.percent_M: 0, ValueType.percent_T: 0},
                          DamageType.moral: {ValueType.row: 0,
                                             ValueType.percent_M: 0, ValueType.percent_T: 0},
                          DamageType.physic: {ValueType.row: 0,
                                              ValueType.percent_M: 0, ValueType.percent_T: 0},
                          DamageType.pure: {ValueType.row: 0,
                                            ValueType.percent_M: 0, ValueType.percent_T: 0}}

        if damage_high is None:
            damage_high = damage_low

        self.__damage_low = damage_low
        self.__damage_high = damage_high
        self.__critical_chance = critical_chance
        self.__critical_value = critical_value

    @property
    def critical_chance(self):
        return self.__critical_chance

    @property
    def critical_value(self):
        return self.__critical_value

    def get(self, damage_type: DamageType, value_type: ValueType = None):
        low_damage = self.__damage_low.get(
            damage_type, {ValueType.row: 0, ValueType.percent_M: 0, ValueType.percent_T: 0})
        high_damage = self.__damage_high.get(damage_type, low_damage.copy())
        if value_type is None:
            return {ReceivedValueType.low: low_damage, ReceivedValueType.high: high_damage}
        low_value = low_damage.get(value_type, 0)
        high_value = high_damage.get(value_type, low_value)
        return {ReceivedValueType.low: low_value, ReceivedValueType.high: high_value,
                ReceivedValueType.calculated:
                    calculate_crit(number_between(low_value, high_value),
                                   self.__critical_chance, self.__critical_value)}

    def activate_boost(self, boost: DamageBoost):
        for damage_type in DamageType:
            if damage_type in self.__damage_low:
                self.__damage_low[damage_type][ValueType.row] = \
                    self.get(damage_type, ValueType.row)[ReceivedValueType.low] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M)) + \
                    boost.get_damage(damage_type, ValueType.row)
                self.__damage_low[damage_type][ValueType.percent_M] = \
                    self.get(damage_type, ValueType.percent_M)[ReceivedValueType.low] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M))
                self.__damage_low[damage_type][ValueType.percent_T] = \
                    self.get(damage_type, ValueType.percent_T)[ReceivedValueType.low] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M))
            if damage_type in self.__damage_high:
                self.__damage_high[damage_type][ValueType.row] = \
                    self.get(damage_type, ValueType.row)[ReceivedValueType.high] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M)) + \
                    boost.get_damage(damage_type, ValueType.row)
                self.__damage_high[damage_type][ValueType.percent_M] = \
                    self.get(damage_type, ValueType.percent_M)[ReceivedValueType.high] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M))
                self.__damage_high[damage_type][ValueType.percent_T] = \
                    self.get(damage_type, ValueType.percent_T)[ReceivedValueType.high] * \
                    (1 + boost.get_damage(damage_type, ValueType.percent_M))
        self.__critical_value += boost.get_crit(Crit.value)
        self.__critical_chance += boost.get_crit(Crit.chance)


class Heal:
    def __init__(self, heal_low: dict = None, heal_high: dict = None,
                 critical_chance: float = 0,
                 critical_value: float = 2):
        if heal_low is None:
            heal_low = {ValueType.row: 0, ValueType.percent_T: 0, ValueType.percent_M: 0}
        if heal_high is None:
            heal_high = heal_low
        self.__heal_low = heal_low
        self.__heal_high = heal_high
        self.__critical_chance = critical_chance
        self.__critical_value = critical_value

    @property
    def critical_chance(self):
        return self.__critical_chance

    @property
    def critical_value(self):
        return self.__critical_value

    def get(self, value_type: ValueType):
        low = self.__heal_low.get(value_type, 0)
        high = self.__heal_high.get(value_type, low)
        return {ReceivedValueType.low: low, ReceivedValueType.high: high,
                ReceivedValueType.calculated:
                    calculate_crit(number_between(low, high),
                                   self.__critical_chance, self.__critical_value)}

    def activate_boost(self, boost: HealBoost):
        self.__heal_low[ValueType.row] = \
            self.__heal_low[ValueType.row] * \
            (1 + boost.get_heal(ValueType.percent_M)) + boost.get_heal(ValueType.row)
        self.__heal_high[ValueType.row] = \
            self.__heal_high[ValueType.row] * \
            (1 + boost.get_heal(ValueType.percent_M)) + boost.get_heal(ValueType.row)
        self.__heal_low[ValueType.percent_M] = \
            self.__heal_low[ValueType.percent_M] * \
            (1 + boost.get_heal(ValueType.percent_M))
        self.__heal_high[ValueType.percent_M] = \
            self.__heal_high[ValueType.percent_M] * \
            (1 + boost.get_heal(ValueType.percent_M))
        self.__heal_low[ValueType.percent_T] = \
            self.__heal_low[ValueType.percent_T] * \
            (1 + boost.get_heal(ValueType.percent_M))
        self.__heal_high[ValueType.percent_T] = \
            self.__heal_high[ValueType.percent_T] * \
            (1 + boost.get_heal(ValueType.percent_M))
        self.__critical_chance += boost.get_crit(Crit.chance)
        self.__critical_value += boost.get_crit(Crit.value)


class Resistance:
    def __init__(self, resistance: dict = None):
        if resistance is None:
            resistance = {DamageType.fire: 0,
                          DamageType.lightning: 0,
                          DamageType.freeze: 0,
                          DamageType.moral: 0,
                          DamageType.physic: 0}
        self.__resistance = resistance

    def set(self, damage_type: DamageType, value: float):
        self.__resistance[damage_type] = value

    def __change(self, damage_type: DamageType, value: float):
        if damage_type not in self.__resistance.keys():
            self.__resistance[damage_type] = 0
        self.__resistance[damage_type] += value

    def up(self, damage_type: DamageType, value: float):
        self.__change(damage_type, value)

    def down(self, damage_type: DamageType, value: float):
        self.__change(damage_type, -value)

    def get(self, damage_type: DamageType):
        if damage_type == DamageType.pure:
            return 0
        return self.__resistance.get(damage_type, 0)

    def activate_boost(self, boost: ResistanceBoost):
        if not boost.enabled:
            for damage_type in DamageType:
                self.set(damage_type=damage_type,
                         value=self.get(damage_type) + boost.get(damage_type))
        boost.enabled = True

    def deactivate_boost(self, boost: ResistanceBoost):
        if boost.enabled:
            for damage_type in DamageType:
                self.set(damage_type=damage_type,
                         value=self.get(damage_type) - boost.get(damage_type))
        boost.enabled = False


class Health:
    def __init__(self, resistance: type, max_health: float, health: float = None):
        self.__max_health = max_health
        if health is None:
            health = max_health
        self.__health = health
        self.__resistance = resistance()

    @property
    def dead(self):
        if self.health > 0:
            return False
        return True

    @property
    def health(self):
        return self.__health

    @property
    def resistance(self):
        return self.__resistance

    @property
    def max_health(self):
        return self.__max_health

    def __set_health(self, value: float):
        self.__health = min(value, self.__max_health)

    def __change_health(self, value: float):
        self.__set_health(min(self.__health + value, self.__max_health))

    def accept_damage(self, damage: Damage):
        if not self.dead:
            total_with_reduce = {}
            for value_type in ValueType:
                total_with_reduce[value_type] = 0
                for damage_type in DamageType:
                    total_with_reduce[value_type] += \
                        damage.get(damage_type, value_type)[ReceivedValueType.calculated] * \
                        (1 - self.__resistance.get(damage_type))
            self.__set_health(self.__health * (1 - total_with_reduce[ValueType.percent_T]))
            self.__change_health(-self.__max_health * total_with_reduce[ValueType.percent_M])
            self.__change_health(-total_with_reduce[ValueType.row])

    def accept_heal(self, heal: Heal):
        if not self.dead:
            self.__set_health(self.health *
                              (1 + heal.get(ValueType.percent_T)[ReceivedValueType.calculated]))
            self.__change_health(self.__max_health *
                                 heal.get(ValueType.percent_M)[ReceivedValueType.calculated])
            self.__change_health(heal.get(ValueType.row)[ReceivedValueType.calculated])

    def refresh_health(self):
        if not self.dead:
            self.__set_health(self.__max_health)

    def resurrect(self):
        """ If animal is dead, res animal with 1 hp"""
        if self.dead:
            self.__set_health(1)

    def __set_max_health(self, value: float):
        self.__max_health = value

    def __change_max_health(self, value: float):
        self.__max_health += value

    def activate_boost(self, boost: HealthBoost):
        if not boost.enabled:
            self.__set_max_health(self.__max_health * (1 + boost.get(ValueType.percent_M)))
            self.__change_max_health(boost.get(ValueType.row))
            self.__health = min(self.__health, self.__max_health)
        boost.enabled = True

    def deactivate_boost(self, boost: HealthBoost):
        if boost.enabled:
            self.__change_max_health(-boost.get(ValueType.row))
            self.__set_max_health(self.__max_health / (1 + boost.get(ValueType.percent_M)))
            self.__health = min(self.__health, self.__max_health)
        boost.enabled = False
