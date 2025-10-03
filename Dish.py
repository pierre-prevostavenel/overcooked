import random
from actions_list import *
from ingredients_list import *


class Dish:
    dishes = [Assemble([Chop(Lettuce), Chop(Tomato)]),]

    def __init__(self, action):
        self.action = action

    def __repr__(self):
        return f"Dish({self.action})"

    def random_dish(cls):
        import random
        return Dish(random.choice(cls.dishes))

    #TODO une fois que l'archi ingrédient est fini, objectif = donner à quel point les deux plats sont simmilaires
    def equal(dish1,dish2):
        return False
