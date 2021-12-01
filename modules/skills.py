from modules.ability import ActiveAbility, PassiveAbility
from modules.animal import Fighter
from modules.bults import BaseAbility


class Skill:
    def __init__(self, name: str, description: str, req_level: int, ability: BaseAbility):
        self.__name = name
        self.__description = description
        self.__req_level = req_level
        self.__ability = ability

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def req_level(self):
        return self.__req_level

    @property
    def ability(self):
        return self.__ability


class ActiveSkill(Skill):
    def __init__(self, name: str, description: str, req_level: int,
                 ability: ActiveAbility):
        super().__init__(name=name, description=description, req_level=req_level,
                         ability=ability)


class PassiveSkill(Skill):
    def __init__(self, name: str, description: str, req_level: int,
                 ability: PassiveAbility):
        super().__init__(name=name, description=description, req_level=req_level,
                         ability=ability)


class SkillTree:
    def __init__(self, skills: list, owner: Fighter):
        self.__skills = skills
        self.__owner = owner

    def get_abilities(self, ability_type: type):
        return [skill.ability for skill in self.__skills
                if skill.req_level <= self.__owner.level and isinstance(skill.ability, ability_type)]

    @property
    def available(self):
        return [skill for skill in self.__skills if skill.req_level <= self.__owner.level]

    @property
    def unavailable(self):
        return [skill for skill in self.__skills if skill.req_level > self.__owner.level]

    @property
    def passive_available(self):
        return [skill for skill in self.__skills
                if skill.req_level <= self.__owner.level and
                isinstance(skill, PassiveSkill)]

    @property
    def active_available(self):
        return [skill for skill in self.__skills
                if skill.req_level <= self.__owner.level and
                isinstance(skill, ActiveSkill)]