from Ingredient import Ingredient
from Action import *
import random

from Ingredient import Ingredient
class Dish:
    dishes = [("Salade",Assemble(Chop(Lettuce()), Chop(Tomato()))),]

    def __init__(self, name, ingredients : list[Ingredient]):
        self.name = name
        self.ingredients = ingredients
        # print(ingredients)

    def __str__(self):
        return f"{self.name}: {self.ingredients}"

    @staticmethod
    def random_dish():
        name, ingredients = random.choice(Dish.dishes)
        return Dish(name, ingredients)

    #TODO une fois que l'archi ingrédient est fini, objectif = donner à quel point les deux plats sont simmilaires
    @staticmethod
    def equal(dish1,dish2):
        return False
