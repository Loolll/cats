import random
from copy import deepcopy


def number_between(a, b):
    return min(a,b) + (max(a,b)-min(a,b))*random.random()


def calculate_crit(value, chance, multiplier):
    if random.random() <= chance:
        return value*multiplier
    return value


