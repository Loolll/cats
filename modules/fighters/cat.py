from modules.abilities.active_damage import Scratch
from modules.abilities.passive_boost import HealthBoost
from modules.animal import Fighter
from modules.bults import MsgType, Voice, ValueType, DamageType, Slot
from modules.features import Health, Resistance, Experience
from modules.skills import SkillTree, PassiveSkill, ActiveSkill
from modules.item import Inventory


class Cat(Fighter):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name=name, age=age, color=color, health=CatHealth, experience=CatExperience,
                         voice=CatVoice, skill_tree=CatSkillTree, inventory=CatInventory)


class CatInventory(Inventory):
    def __init__(self, owner):
        super().__init__(owner=owner, max_size=3, slots=
        {Slot.boots: None, Slot.head: None, Slot.gloves: None, Slot.body: None})


class CatExperience(Experience):
    def __init__(self):
        max_level = 20
        exp_road = [0, 1, 4, 8, 13, 20,
                    27, 35, 46, 60, 76,
                    96, 120, 150, 190, 240,
                    290, 360, 450, 590, 800]
        super().__init__(max_level=max_level, exp_road=exp_road)


class CatVoice(Voice):
    def __init__(self):
        messages = {MsgType.hello: ["Hi, i'm super cat"],
                    MsgType.die: ["Sad"],
                    MsgType.deal_damage: ["MYAU"],
                    MsgType.take_damage: ["myau("],
                    MsgType.restore: ["MMMM"],
                    MsgType.resurrect: ["kek"]}
        super().__init__(messages=messages)


class CatResistance(Resistance):
    def __init__(self):
        resistance = {
            DamageType.physic: 0.1,
            DamageType.freeze: 0.3,
            DamageType.fire: 0,
            DamageType.lightning: 0.5,
            DamageType.moral: 0.5
        }
        super().__init__(resistance=resistance)


class CatHealth(Health):
    def __init__(self):
        max_health = 1000
        super().__init__(resistance=CatResistance, max_health=max_health)


class CatSkillTree(SkillTree):
    def __init__(self, owner: Cat):
        skill1 = ActiveSkill(name="Атака1",
                             description="Ваш кот осваивает азы сражений."
                                         "Позволяет использовать способность царапнуть I уровня.",
                             req_level=1, ability=Scratch(10, 15, critical_chance=0.25,
                                                          critical_value=2, name="Царапнуть I"))
        skill2 = ActiveSkill(name="Атака2",
                             description="Ваш кот становится сильнее."
                                         "Позволяет использовать способность царапнуть II уровня.",
                             req_level=5, ability=Scratch(17, 25, critical_chance=0.3,
                                                          critical_value=2.5, name="Царапнуть II"))
        skill3 = PassiveSkill(name="Улучшение1",
                              description="Ваш кот слишком часто прыгает с подоконника,"
                                          "он натренировался падать, теперь его здоровье выше.",
                              req_level=3, ability=
                              HealthBoost(
                                  description="Увеличивает здоровье на 100",
                                  value={ValueType.row: 100},
                                  name="СтойкостьI")
                              )
        skills = [skill1, skill2, skill3]
        super().__init__(skills=skills, owner=owner)
