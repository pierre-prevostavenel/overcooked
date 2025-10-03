from Ingredient import Ingredient
import random

class Dish:
    dishes = [("Salad", [Ingredient("Chopped Lettuce"), Ingredient("Chopped Tomato")])]

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return f"{self.name}: {self.ingredients}"

    @staticmethod
    def random_dish():
        name, ingredients = random.choice(Dish.dishes)
        return Dish(name, ingredients)

    #TODO une fois que l'archi ingrédient est fini, objectif = donner à quel point les deux plats sont simmilaires
    @staticmethod
    def equal(dish1,dish2):
        return False
