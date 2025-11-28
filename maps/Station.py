# Station.py
from food.Ingredient import Ingredient
from maps.Tile import Tile


class Station(Tile):
    """Base class pour les stations."""
    def __init__(self, row, col, name, action, tile_size=50):
        self.name = name
        self.action = action
        super().__init__(row, col, tile_type=name, tile_size=tile_size)

    def interact(self, player):
        durations = {
            "fetch": 1,
            "cook": 5,
            "fry": 6,
            "chop": 4,
            "wash": 4,
            "plate": 1,
        }

        if getattr(player, "interaction_progress", 0) == 0:
            player.interaction_progress = durations.get(self.action, 5)
            return player.interaction_progress

        player.interaction_progress = max(player.interaction_progress - 1, 0)

        if player.interaction_progress == 0:
            try:
                self.perform(player)
            except Exception as exc:
                print(f"Error performing action on {self.name}: {exc}")
            return 0

        return player.interaction_progress

    def perform(self, player):
        return


class Workbench(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "workbench", action="cook", tile_size=tile_size)

    def perform(self, player):
        """Called when chop completes: try to chop the held ingredient.
        """
        if player.itemHeld is not None:
            ingredient = player.itemHeld
            chopped_ingredient = ingredient.chop()
            if chopped_ingredient:
                player.itemHeld = chopped_ingredient
                print(f"{player} chopped {ingredient} into {chopped_ingredient} at the gas station.")
                print(f"{player} now holds {player.itemHeld}.")
            else:
                print(f"{ingredient} cannot be chopped.")
        else:
            print(f"{player} has nothing to chop.")


class Fridge(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "fridge", action="fetch", tile_size=tile_size)

    def perform(self, player):
        if player.itemWanted is not None:
            ingredient_obj = Ingredient(player.itemWanted, "raw")
            player.grab(ingredient_obj)
            print(f"Fridge gave {ingredient_obj} to {player}")


class Oven(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "oven", action="cook", tile_size=tile_size)

    def perform(self, player):
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


class WhiteSink(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "white_sink", action="wash", tile_size=tile_size)

    def perform(self, player):
        if player.itemHeld is not None:
            ingredient = player.itemHeld
            washed_ingredient = ingredient.wash()
            if washed_ingredient:
                player.itemHeld = washed_ingredient
                print(f"{player} washed {ingredient} into {washed_ingredient} at the sink.")
                print(f"{player} now holds {player.itemHeld}.")
            else:
                print(f"{ingredient} cannot be washed.")
        else:
            print(f"{player} has nothing to wash.")
