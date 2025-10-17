import json
import random
from Ingredient import Ingredient
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

    @staticmethod
    def equal(dish1, dish2):
        """Compare le nombre d’occurrences de chaque ingrédient"""
        def count_ingredients(ingredients):
            c = {}
            for i in ingredients:
                c[i] = c.get(i, 0) + 1
            return c
        return count_ingredients(dish1.ingredients) == count_ingredients(dish2.ingredients)

    @staticmethod
    def init():
        """Charge tous les plats depuis food.json automatiquement"""
        json_path = os.path.join(os.path.dirname(__file__), "food.json")
        with open(json_path, "r") as f:
            data = json.load(f)

        for dish_data in data.get("dishes", []):
            dish_name = dish_data["name"]
            ingredients = [
                Ingredient(ing["name"], ing["state"])
                for ing in dish_data.get("ingredients", [])
            ]
            Dish.dishes.append((dish_name, ingredients))
