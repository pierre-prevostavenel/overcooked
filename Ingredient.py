import json
from Item import Item

# charger le JSON une seule fois
with open("food.json") as f:
    FOOD_DATA = json.load(f)["ingredients"]

class Ingredient(Item):
    def __init__(self, name: str, state: str = "raw", rect=(0,0,50,50), image_path=None, fallback_color=(255,255,255), layer=0):
        super().__init__(name, rect=rect, image_path=image_path, fallback_color=fallback_color, layer=layer)
        self.state = state

    def _get_actions(self):
        """Récupère le dictionnaire actions pour cet ingredient et cet état"""
        ing_data = next((ing for ing in FOOD_DATA if ing["name"] == self.name), None)
        if not ing_data:
            return {}
        state_data = next((s for s in ing_data["states"] if s["state"] == self.state), None)
        if not state_data:
            return {}
        return state_data.get("actions", {})

    def _transform(self, action: str):
        actions = self._get_actions()
        if action in actions:
            result = actions[action]
            return Ingredient(
                result["name"], 
                result["state"], 
                rect=self.rect,
                image_path=None,           # <-- mettre None
                fallback_color=(255,255,255), 
                layer=self._layer
            )
        print(f"Action '{action}' has no effect on {self}")
        return None
    
    # les actions que player peut effectuer sur cet ingrédient (ils return None si pas possible)
# --------------------------------------------------------------------

    def cook(self):
        return self._transform("cook")

    def chop(self):
        return self._transform("chop")  # action "chop" dans le JSON

# --------------------------------------------------------------------

    def as_tuple(self):
        return (self.name, self.state)
    
    def __str__(self):
        return f"{self.name} ({self.state})"
