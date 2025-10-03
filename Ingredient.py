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
    def get_super_name(self):
        return "Ingredient"

# Potato ----------------------------------------------
class Potato(Ingredient):
    def __init__(self):
        super().__init__("Potato")

    def chop(self):
        return ChoppedPotato()

    def cook(self):
        return CookedPotato()
    
class CookedPotato(Ingredient):
    def __init__(self):
        super().__init__("Cooked Potato")


class ChoppedPotato(Ingredient):
    def __init__(self):
        super().__init__("Chopped Potato")

    def fry(self):
        return Fries()
    

class Fries(Ingredient):
    def __init__(self):
        super().__init__("Fries")


# Tomato ----------------------------------------------
class Tomato(Ingredient):
    def __init__(self):
        super().__init__("Tomato")

    def chop(self):
        return ChoppedTomato()


class ChoppedTomato(Ingredient):
    def __init__(self):
        super().__init__("Chopped Tomato")


# Lettuce ----------------------------------------------
class Lettuce(Ingredient):
    def __init__(self):
        super().__init__("Lettuce")

    def chop(self):
        return ChoppedLettuce()


class ChoppedLettuce(Ingredient):
    def __init__(self):
        super().__init__("Chopped Lettuce")


# Steak ----------------------------------------------
class Steak(Ingredient):
    def __init__(self):
        super().__init__("Steak")

    def cook(self):
        return CookedSteak()


class CookedSteak(Ingredient):
    def __init__(self):
        super().__init__("Cooked Steak")


