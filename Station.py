# Station.py
from Tile import Tile

class Station(Tile):
    """Base class pour les stations."""
    def __init__(self, row, col, name, action, tile_size=50):
        self.name = name
        self.action = action  # "cook", "fetch", "chop"...
        super().__init__(row, col, tile_type=name, tile_size=tile_size)

class Workbench(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "workbench", action="cook", tile_size=tile_size)

class Fridge(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "fridge", action="fetch", tile_size=tile_size)

    def interact(self, player, ingredient):
        """Permet au player de récupérer un ingrédient."""
        # Exemple simple : toujours donner un "tomato" cru
        if player.itemHeld is None:
            player.grab(ingredient)
            print(f"{player} was given {ingredient} from the fridge.")
        else:
            print(f"{player} cannot pick up item; hands are full.")

class GasStation(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "gas_station", action="cook", tile_size=tile_size)

    def interact(self, player):
        """Permet au player de cuisiner un ingrédient."""
        if player.itemHeld is not None:
            ingredient = player.itemHeld
            cooked_ingredient = ingredient.cook()
            if cooked_ingredient:
                player.itemHeld = cooked_ingredient
                print(f"{player} cooked {ingredient} into {cooked_ingredient} at the gas station.")
            else:
                print(f"{ingredient} cannot be cooked.")
        else:
            print(f"{player} has nothing to cook.")
