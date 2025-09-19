class Ingredient:
    def __init__(self, name, next_stages=None):
        self.name = name
        self.next_stages = next_stages or [] 

    def evolve(self, next_ingredient):
        if next_ingredient in self.next_stages:
            return next_ingredient
        else:
            print(f"Cannot evolve {self} to {next_ingredient}!")
            return self

    def __repr__(self):
        return self.name