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

class IngredientGraph:
    transitions = {}
    @staticmethod
    def add(name, state, transformations):
        src = (name, state)
        for action, result in transformations.items():
            new_name = result["name"]
            new_state = result["state"]
            dst = (new_name, new_state)
            if dst in IngredientGraph.transitions:
                IngredientGraph.transitions[dst].append((src, action))
            else:
                IngredientGraph.transitions[dst] = [(src, action)]

                
    @staticmethod
    def get_plan(goal):
        """Retourne un plan d'action pour atteindre le goal (name, state)"""
        plans = []
        visited = set()

        def dfs(current, path):
            if current in visited:
                return
            visited.add(current)
            if not current in IngredientGraph.transitions:
                plans.append(path[::-1])
                return
            for src, action in IngredientGraph.transitions[current]:
                dfs(src, path + [(action, current)])

        dfs(goal, [])
        return plans

    @staticmethod
    def init(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)

            for ing_name, trans_state in data["ingredients"].items():
                for state, trans in trans_state.items():
                    IngredientGraph.add(ing_name, state, trans)
                    