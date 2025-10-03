from Ingredient import Ingredient

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
