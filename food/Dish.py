import json
import random

from food.Ingredient import Ingredient


class Dish:
    dishes = []

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
        def count_ingredients(ingredients):
            counts = {}
            for item in ingredients:
                counts[item] = counts.get(item, 0) + 1
            return counts

        return count_ingredients(dish1.ingredients) == count_ingredients(dish2.ingredients)

    @staticmethod
    def init(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        Dish.dishes.clear()
        for dish_data in data.get("dishes", []):
            dish_name = dish_data["name"]
            ingredients = [
                Ingredient(ing["name"], ing["state"])
                for ing in dish_data.get("ingredients", [])
            ]
            Dish.dishes.append((dish_name, ingredients))


class Plate(Dish):
    def __init__(self, name):
        super().__init__(name, [])

    def add_ingr(self, ingr):
        self.ingredients.append(ingr)

    def verify(self, order):
        return Dish.equal(self, order)
