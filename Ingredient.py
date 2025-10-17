import json

class Ingredient:
    def __init__(self, name, state="raw", transformations={}):
        self.name = name
        self.state = state
        self.transformations = transformations  # action -> (new_name, new_state)

    def apply_action(self, action):
        if action in self.transformations:
            new_name, new_state = self.transformations[action]
            self.name = new_name
            self.state = new_state
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
    
    @staticmethod
    def equal(i1,i2):
        return (i1.name == i2.name) and (i1.state == i2.state) 
    
    def __hash__(self):
        return hash((self.name, self.state))
                    