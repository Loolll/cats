from modules.fighters.cat import Cat
from modules.place import Place
from modules.animal import ActiveFighter
from modules.items.heads import Helmet
from modules.items.boots import Boots
from modules.items.gloves import Gloves, Gloves1
from modules.bults import Slot
from modules.ability import BoostAbility, PassiveBoostAbility
from modules.abilities.passive_boost import Stamina, CritBoost, Crit, FireDamageBoost


cat1 = Cat("Кошка-ебанная", age=3, color="red")
cat2 = Cat("Vasya", age=10, color='white')
place = Place("Home", "xd", "home", [Stamina(100), FireDamageBoost(300)])

cat1._experience.add_exp(1000)

print(cat1.inventory.backpack)
print(cat2.inventory.backpack)
gloves = Gloves1()
cat1.inventory.add(gloves)
cat1.inventory.put_on(gloves)
print(cat1.inventory.slots)
print(cat2.inventory.slots)

with ActiveFighter(cat1, place) as fcat1, ActiveFighter(cat2, place) as fcat2:
    print(cat1.active_abilities)
    ab1 = cat1.active_abilities[1]
    ab2 = cat2.active_abilities[0]
    print(fcat1.health, fcat1.max_health)
    print(fcat2.health, fcat2.max_health)
    while not fcat1.dead and not fcat2.dead:
        fcat1.use_active_ability(ab1, fcat2)
        fcat2.use_active_ability(ab2, fcat1)
        print(fcat1.health, fcat2.health)


# with ActiveFighter(cat1, place) as fcat1:
#     pass