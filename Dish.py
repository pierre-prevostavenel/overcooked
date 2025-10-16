from Ingredient import Ingredient
from Action import *
import random

from Ingredient import Ingredient
class Dish:
    dishes = []

    def __init__(self, name, ingredients : list[Ingredient]):
        self.name = name
        self.ingredients = ingredients
        # print(ingredients)

    def __str__(self):
        buff = f"{self.name}: "
        for i in self.ingredients :
            buff += " " + i.__str__()
        return buff

    @staticmethod
    def random_dish():
        name, ingredients = random.choice(Dish.dishes)
        return Dish(name, ingredients)

    # TODO voir pour implémenter un systéme de score plus avancé
    @staticmethod
    def equal(dish1, dish2):
        # on veut le même nb d'occ d'ingrédient dans chaque plat
        def count_ingredients(ingredients):
            c = {}
            for i in ingredients:
                if(i in c):
                    c[i] += 1
                else :
                    c[i] = 1
            return c
        c1 = count_ingredients(dish1.ingredients)
        c2 = count_ingredients(dish2.ingredients)
        return c1 == c2

    @staticmethod
    def init(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        
        for dish_name, required_ingredients in data["dish"].items():
            ingredients = [
                Ingredient(
                    ing["name"],
                    ing["state"]
                )
                for ing in required_ingredients
            ]
            Dish.dishes.append((dish_name, ingredients))

