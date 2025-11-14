# Station.py
from food.Ingredient import Ingredient
from maps.Tile import Tile

class Station(Tile):
    """Base class pour les stations.

    interact(player) now implements a simple interaction countdown using
    `player.interaction_progress`. On the first call it sets the duration
    according to the station action (fetch/cook/chop/plate). Subsequent calls
    decrement the counter and when it reaches 0 the station's `perform`
    method is called to apply the effect (e.g. fridge spawns an ingredient,
    oven cooks an ingredient).

    The return value of `interact` is the remaining ticks (int). 0 means the
    action has just completed (and `perform` was executed).
    """
    def __init__(self, row, col, name, action, tile_size=50):
        self.name = name
        self.action = action  # "cook", "fetch", "chop"...
        super().__init__(row, col, tile_type=name, tile_size=tile_size)

    def interact(self, player):
        """Handle timed interaction and return remaining ticks.

        - On first call (player.interaction_progress == 0) this sets the
          interaction duration based on the station action and returns it.
        - On subsequent calls it decrements the counter and when it reaches
          0 calls ``self.perform(player)`` and returns 0.

        This design keeps timing state on the player (so a player can only
        perform a single interaction at a time) while allowing stations to
        define their final effect by overriding `perform`.
        """
        # default durations (ticks) per action
        durations = {
            "fetch": 1,
            "cook": 5,
            "chop": 5,
            "plate": 1,
        }

        # If no interaction in progress, start one and return duration
        if getattr(player, "interaction_progress", 0) == 0:
            player.interaction_progress = durations.get(self.action, 5)
            return player.interaction_progress

        # Otherwise continue the interaction (decrement)
        player.interaction_progress -= 1
        if player.interaction_progress < 0:
            player.interaction_progress = 0

        # If finished, perform station-specific effect and return 0
        if player.interaction_progress == 0:
            try:
                self.perform(player)
            except Exception as e:
                print(f"Error performing action on {self.name}: {e}")
            return 0

        # Still in progress: return remaining ticks
        return player.interaction_progress

    def perform(self, player):
        return

class Workbench(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "workbench", action="cook", tile_size=tile_size)

class Fridge(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "fridge", action="fetch", tile_size=tile_size)

    def perform(self, player):
        """Create the Ingredient when the interaction finishes and give it to
        the player.
        """
        if player.itemWanted is not None:
            ingredient_obj = Ingredient(player.itemWanted, "raw")
            player.grab(ingredient_obj)
            print(f"Fridge gave {ingredient_obj} to {player}")

class Oven(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "oven", action="cook", tile_size=tile_size)

    def perform(self, player):
        """Called when cooking completes: try to cook the held ingredient.
        """
        if player.itemHeld is not None:
            ingredient = player.itemHeld
            cooked_ingredient = ingredient.cook()
            if cooked_ingredient:
                player.itemHeld = cooked_ingredient
                print(f"{player} cooked {ingredient} into {cooked_ingredient} at the gas station.")
                print(f"{player} now holds {player.itemHeld}.")
            else:
                print(f"{ingredient} cannot be cooked.")
        else:
            print(f"{player} has nothing to cook.")
