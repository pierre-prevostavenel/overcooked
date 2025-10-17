import json

with open("food.json") as f:
    DATA = json.load(f)

class Ingredient:
    def __init__(self, name, state="raw", transformations=None):
        self.name = name
        self.state = state

        # Si aucune transformation n'est donnée, on la récupère du JSON
        if transformations is None:
            self.transformations = self._load_transformations_from_data()
        else:
            self.transformations = transformations

    def _load_transformations_from_data(self):
        # Cherche l'ingrédient dans le JSON
        if self.name in DATA["ingredients"]:
            ingredient_data = DATA["ingredients"][self.name]
            # Si on est en état raw et que des transformations existent
            if self.state in ingredient_data:
                return {
                    action: (info["name"], info["state"])
                    for action, info in ingredient_data[self.state].items()
                }
        return {}

    def apply_action(self, action):
        if action in self.transformations:
            new_name, new_state = self.transformations[action]
            self.name = new_name
            self.state = new_state
            self.transformations = self._load_transformations_from_data()
        else:
            print(f"Action '{action}' has no effect on {self}")

    def get_possible_actions(self):
        return list(self.transformations.keys())

    def as_tuple(self):
        return (self.name, self.state)

    def __str__(self):
        return f"{self.name} ({self.state})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return (self.name == other.name) and (self.state == other.state) 
        return False
    
    def __hash__(self):
        return hash((self.name, self.state))
