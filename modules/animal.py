from modules.ability import PassiveBoostAbility, ActiveBoostAbility, ActiveAbility
from modules.bults import BaseAnimal, BoostType
from modules.exceptions import *
from modules.features import LeaderExperience
from modules.place import Place
from modules.tools import deepcopy


class Animal(BaseAnimal):
    """ Provides base entity of alive object """

    def __init__(self, name: str, age: int, color: str):
        self.__name = name
        self.__age = age
        self.__color = color

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def color(self):
        return self.__color

    def rename(self, name: str):
        self.__name = name


class Fighter(Animal):
    """ Provides base entity of fighter object.
        We have voice, skill tree, inventory, health, experience models in it """
    def __init__(self, name: str, age: int, color: str, health: type, experience: type,
                 voice: type, skill_tree: type, inventory: type):
        super().__init__(name=name, age=age, color=color)
        self.__skill_tree = skill_tree(self)
        self.__inventory = inventory(self)
        self.__voice = voice()
        self._experience = experience()
        self._health = health()
        self.__activated_passive_boosts = set()

    @property
    def __passive_boosts(self):
        return self.__skill_tree.get_abilities(PassiveBoostAbility) + \
               self.__inventory.get_abilities(PassiveBoostAbility)

    @property
    def active_boosts(self):
        return self.__skill_tree.get_abilities(ActiveBoostAbility) + \
               self.__inventory.get_abilities(ActiveBoostAbility)

    @property
    def active_abilities(self):
        return self.__skill_tree.get_abilities(ActiveAbility) + \
               self.__inventory.get_abilities(ActiveAbility)

    def _activate_passive_boost(self, boost: PassiveBoostAbility):
        if boost not in self.__activated_passive_boosts:
            if boost.kind == BoostType.experience:
                self._experience.activate_boost(boost)
            elif boost.kind == BoostType.resistance:
                self._health.resistance.activate_boost(boost)
            elif boost.kind == BoostType.health:
                self._health.activate_boost(boost)
            else:
                return
            self.__activated_passive_boosts.add(boost)

    def _deactivate_passive_boost(self, boost: PassiveBoostAbility):
        if boost in self.__activated_passive_boosts:
            if boost.kind == BoostType.experience:
                self._experience.deactivate_boost(boost)
            elif boost.kind == BoostType.resistance:
                self._health.resistance.deactivate_boost(boost)
            elif boost.kind == BoostType.health:
                self._health.deactivate_boost(boost)
            else:
                return
            self.__activated_passive_boosts.remove(boost)

    def _activate_self_passive_boosts(self):
        boosts = self.__passive_boosts
        for boost in boosts:
            self._activate_passive_boost(boost)

    def _deactivate_self_passive_boosts(self):
        boosts = self.__passive_boosts
        for boost in boosts:
            self._deactivate_passive_boost(boost)

    @property
    def money(self):
        return self.money

    @property
    def level(self):
        return self._experience.level

    @property
    def max_level(self):
        return self._experience.max_level

    @property
    def for_next_level(self):
        return self._experience.for_next_level

    @property
    def voice(self):
        return self.__voice

    @property
    def skill_tree(self):
        return self.__skill_tree

    @property
    def inventory(self):
        return self.__inventory

    @property
    def dead(self):
        return self._health.dead

    def resurrect(self):
        self._health.resurrect()


class ActiveFighter:
    """ This class is wrapper over Fighter object.
        We should use it when fight. """
    __created = set()

    def __init__(self, fighter: Fighter, place: Place):
        if fighter in type(self).__created:
            raise MultiplyFighterError
        type(self).__created.add(fighter)
        if not fighter.dead:
            self.__fighter = fighter
            self.__place_passive_boosts = deepcopy(place.passive_boosts)
            self.__active_boosts = self.__fighter.active_boosts + deepcopy(place.active_boosts)
        else:
            raise DeadException

    def __enter__(self):
        self.__fighter._activate_self_passive_boosts()
        for boost in self.__place_passive_boosts:
            self.__fighter._activate_passive_boost(boost)
        self.__fighter._health.refresh_health()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__fighter._deactivate_self_passive_boosts()
        for boost in self.__place_passive_boosts:
            self.__fighter._deactivate_passive_boost(boost)
        type(self).__created.remove(self.__fighter)

    def use_active_ability(self, ability: ActiveAbility, target):
        if ability in self.__fighter.active_abilities:
            ability.activate(sender=self, target=target)
        else:
            raise AbilityError

    def accept_damage(self, damage):
        self.__fighter._health.accept_damage(damage)

    def accept_heal(self, heal):
        self.__fighter._health.accept_heal(heal)

    @property
    def dead(self):
        return self.__fighter.dead

    @property
    def health(self):
        return self.__fighter._health.health

    @property
    def max_health(self):
        return self.__fighter._health.max_health

    def make_damage(self, damage, target):
        for boost in self.__active_boosts:
            if boost.kind == BoostType.damage:
                damage.activate_boost(boost)
        target.accept_damage(damage)

    def make_heal(self, heal, target):
        for boost in self.__active_boosts:
            if boost.kind == BoostType.heal:
                heal.activate_boost(boost)
        target.accept_heal(heal)

    def exp_earn(self, exp):
        self.__fighter._experience.add_exp(exp)

    @property
    def voice(self):
        return self.__fighter.voice


class Leader(Animal):
    """ Provides Leader for group of fighters """
    __used_fighters = set()

    def __init__(self, name: str, age: int, color: str, exp: int = 1,
                 money: float = 0, place: Place = None):
        super().__init__(name=name, age=age, color=color)
        self.__fighters = set()
        self.__experience = LeaderExperience(exp)
        self.__place = place
        self.__money = money
        self.__in_with = False

    @property
    def max_fighter_slots(self):
        return self.__experience.level

    def add_fighter(self, fighter: Fighter):
        self.__in_with_req(False)
        if len(self.__fighters) >= self.max_fighter_slots:
            raise NotEnoughFighterSlotException
        if fighter in type(self).__used_fighters:
            raise MultiplyFighterError
        self.__fighters.add(fighter)
        type(self).__used_fighters.add(fighter)

    def remove_fighter(self, fighter: Fighter):
        self.__in_with_req(False)
        if fighter not in self.__fighters:
            raise InvalidFighter
        self.__fighters.remove(fighter)
        type(self).__used_fighters.remove(fighter)

    def go_on_place(self, place: Place):
        self.__in_with_req(False)
        self.__place = place

    def __enter__(self):
        self.__in_with_req(False)
        self.__enter_fighters()
        self.__in_with = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__in_with_req(True)
        self.__exit_fighters(exc_type, exc_val, exc_tb)
        self.__in_with = False

    def __enter_fighters(self):
        """Makes ActiveFighters from all fighters -> Produce __enter__ for it"""
        self.__in_with_req(False)
        if self.__place is None:
            raise NoPlaceError
        active_fighters = set()
        for fighter in self.__fighters:
            active_fighters.add(ActiveFighter(fighter, self.__place).__enter__())
        self.__active_fighters = active_fighters

    def __exit_fighters(self, exc_type, exc_val, exc_tb):
        """Ends all ActiveFighters -> Produce __exit__ for it"""
        self.__in_with_req(True)
        for active_fighter in self.__active_fighters:
            active_fighter.__exit__(exc_type, exc_val, exc_tb)
        self.__active_fighters = set()

    def refresh_active_abilities(self):
        self.__active_abilities = set()
        self.__active_ability_linker = {}
        for fighter in self.__fighters:
            if not fighter.dead:
                for ability in fighter.active_abilities:
                    self.__active_abilities.add(ability)
                    self.__active_ability_linker[ability] = fighter

    def refresh_items(self):
        self.__in_with_req(False)
        self.__inventories = set()
        self.__items = set()
        self.__item_linker = {}
        self.__inventory_linker = {}
        for fighter in self.__fighters:
            inventory = fighter.inventory
            self.__inventories.add(inventory)
            self.__inventory_linker[inventory] = fighter
            for item in inventory.backpack:
                self.__items.add(item)
                self.__item_linker[item] = inventory

    def sell_item(self, item):
        self.__in_with_req(False)
        try:
            self.__earn_money(self.__item_linker[item].sell_item())
        except (KeyError, NotInInventoryError):
            raise WrongItemError

    def use_active_ability(self, ability: ActiveAbility, target):
        self.__in_with_req(True)
        self.__active_ability_linker[ability].use_active_ability(ability=ability, target=target)

    def earn_exp(self, exp: float):
        """Divide all received exp to self fighters"""
        self.__in_with_req(True)
        self.__experience.add_exp(exp)
        for active_fighter in self.__active_fighters:
            active_fighter.earn_exp(exp / len(self.__active_fighters))

    @property
    def active_fighters(self):
        self.__in_with_req(True)
        return self.__active_fighters

    def __earn_money(self, money):
        self.__money += money

    def __in_with_req(self, status=True):
        """Function which requires $status in_with station.
            Raises NotInWithError, InWithError."""
        if self.__in_with != status:
            if not self.__in_with:
                raise NotInWithError
            raise InWithError

    @property
    def defeated(self):
        return all([fighter.dead for fighter in self.__fighters])
