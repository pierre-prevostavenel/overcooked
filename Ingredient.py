from abc import ABC, abstractmethod

class Ingredient(ABC):
    def __init__(self, name):
        self.name = name
        self.previous = None  # (Ingredient, action)

    def chop(self):
        return False

    def cook(self):
        return False

    def fry(self):
        return False

    def __repr__(self):
        return self.name
    


