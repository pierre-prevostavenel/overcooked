from Ingredient import Ingredient
class Dish:
    def __init__(self, name, ingredients : list[Ingredient]):
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return f"{self.name}: {self.ingredients}"