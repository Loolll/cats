from modules.bults import BasePlace
from modules.ability import ActiveBoostAbility, PassiveBoostAbility


class Place(BasePlace):
    def __init__(self, name: str, description: str, color:str, boosts: list = None):
        if boosts is None:
            boosts = []
        self.__name = name
        self.__description = description
        self.__boosts = boosts
        self.__color = color

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def color(self):
        return self.__color

    @property
    def active_boosts(self):
        return [ability for ability in self.__boosts if isinstance(ability, ActiveBoostAbility)]

    @property
    def passive_boosts(self):
        return [ability for ability in self.__boosts if isinstance(ability, PassiveBoostAbility)]


