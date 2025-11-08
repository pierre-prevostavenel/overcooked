import json
import random
from food.Ingredient import Ingredient
import os

class Dish:
    dishes = []  # liste des tuples (name, list[Ingredient])

    def __init__(self, name: str, ingredients: list[Ingredient]):
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return f"{self.name}: " + ", ".join(str(i) for i in self.ingredients)

    @staticmethod
    def random_dish():
        name, ingredients = random.choice(Dish.dishes)
        return Dish(name, ingredients)

    # TODO voir pour implémenter un système de score plus avancé
    @staticmethod
    def equal(dish1, dish2):
        """Compare le nombre d’occurrences de chaque ingrédient"""
        def count_ingredients(ingredients):
            c = {}
            for i in ingredients:
                c[i] = c.get(i, 0) + 1
            return c
        
        c1 = count_ingredients(dish1.ingredients)
        c2 = count_ingredients(dish2.ingredients)
        print(c1,c2)
        return c1 == c2

    @staticmethod
    def init(json_path):
        """Charge tous les plats depuis food.json automatiquement"""
        with open(json_path, "r") as f:
            data = json.load(f)

        for dish_data in data.get("dishes", []):
            dish_name = dish_data["name"]
            ingredients = [
                Ingredient(ing["name"], ing["state"])
                for ing in dish_data.get("ingredients", [])
            ]
            Dish.dishes.append((dish_name, ingredients))
        
        # V2
        # for dish_name, required_ingredients in data["dish"].items():
        #     ingredients = [
        #         Ingredient(
        #             ing["name"],
        #             ing["state"]
        #         )
        #         for ing in required_ingredients
        #     ]
        #     Dish.dishes.append((dish_name, ingredients))


class Plate(Dish):
    def __init__(self, name):
        super().__init__(name, [])
    def add_ingr(self, ingr):
        self.ingredients.append(ingr)
    def verify(self, order):
        return Dish.equal(self, order)
