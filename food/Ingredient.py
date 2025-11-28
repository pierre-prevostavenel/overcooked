import json

from maps.Item import Item

FOOD_DATA = None


class Ingredient(Item):
    def __init__(self, name: str, state: str = "raw", rect=(0, 0, 50, 50), fallback_color=(255, 255, 255), layer=0):
        image_path = self._get_image_path(name, state)
        super().__init__(name, rect=rect, image_path=image_path, fallback_color=fallback_color, layer=layer)
        self.state = state

    @staticmethod
    def init(json_path):
        """Charge la description des ingrédients à partir du JSON."""
        global FOOD_DATA
        with open(json_path, "r", encoding="utf-8") as f:
            FOOD_DATA = json.load(f)["ingredients"]

    @staticmethod
    def _get_image_path(name, state):
        if FOOD_DATA is None:
            raise RuntimeError("Ingredient.init(json_path) doit être appelé avant de créer un ingrédient.")
        ing_data = next((ing for ing in FOOD_DATA if ing["name"] == name), None)
        if not ing_data:
            raise ValueError(f"Ingrédient '{name}' non trouvé dans le JSON")
        state_data = next((s for s in ing_data["states"] if s["state"] == state), None)
        if not state_data:
            raise ValueError(f"État '{state}' pour '{name}' non trouvé dans le JSON")
        image = state_data.get("image")
        if not image:
            raise ValueError(f"Pas d'image définie pour '{name}' à l'état '{state}'")
        return f"assets/ingredients/{image}"

    def _get_actions(self):
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
            return Ingredient(result["name"], result["state"], rect=self.rect, fallback_color=(255, 255, 255), layer=self._layer)
        print(f"Action '{action}' has no effect on {self}")
        return None

    def cook(self):
        return self._transform("cook")

    def wash(self):
        return self._transform("wash")

    def brew(self):
        return self._transform("brew")

    def chop(self):
        return self._transform("chop")

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