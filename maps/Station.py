from food.Ingredient import Ingredient
from maps.Tile import Tile

class Station(Tile):
    def __init__(self, row, col, name, action, tile_size=50):
        self.name = name
        self.action = action  # "cook", "fetch", "chop", "plate"…
        self.itemHeld = None  # Objet actuellement sur la station
        super().__init__(row, col, tile_type=name, tile_size=tile_size)

    def interact(self, player):
        """Interaction classique pour les stations qui stockent l’objet."""
        durations = {
            "fetch": 1,
            "cook": 5,
            "chop": 5,
            "plate": 1,
            "wash": 5,
        }

        if getattr(player, "interaction_progress", 0) == 0:
            player.interaction_progress = durations.get(self.action, 5)
            if self.action != "fetch":  # fetch est réservé à la Fridge
                self.itemHeld = player.itemHeld
                player.itemHeld = None
            return player.interaction_progress

        player.interaction_progress -= 1
        if player.interaction_progress < 0:
            player.interaction_progress = 0

        if player.interaction_progress == 0:
            try:
                self.perform(player)
                if self.action != "fetch":  # restituer l'objet sauf pour la Fridge
                    player.itemHeld = self.itemHeld
                    self.itemHeld = None
            except Exception as e:
                print(f"Error performing action on {self.name}: {e}")
            return 0

        return player.interaction_progress

    def perform(self, player):
        """À surcharger pour l'effet final de la station."""
        return
    
    def draw(self, surface):
        # dessine la tuile de base (Tile)
        surface.blit(self.image, self.rect.topleft)
        
        # si la station a un itemHeld, le dessiner au centre
        if self.itemHeld is not None:
            item_rect = self.itemHeld.image.get_rect(center=self.rect.center)
            surface.blit(self.itemHeld.image, item_rect.topleft)


# Stations spécifiques
class Workbench(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "workbench", action="chop", tile_size=tile_size)

class Oven(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "oven", action="cook", tile_size=tile_size)

    def perform(self, player):
        if player.itemHeld is not None:
            cooked = player.itemHeld.cook()
            if cooked:
                player.itemHeld = cooked
                print(f"{player} cooked the ingredient into {cooked}.")
            else:
                print(f"{player.itemHeld} cannot be cooked.")

class WhiteSink(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "white_sink", action="wash", tile_size=tile_size)

    def perform(self, player):
        if player.itemHeld is not None:
            washed = player.itemHeld.wash()
            if washed:
                player.itemHeld = washed
                print(f"{player} washed the ingredient into {washed}.")
            else:
                print(f"{player.itemHeld} cannot be washed.")

class Fridge(Station):
    def __init__(self, row, col, tile_size=50):
        super().__init__(row, col, "fridge", action="fetch", tile_size=tile_size)

    def interact(self, player):
        """Fridge spéciale : donne directement l'ingrédient au player."""
        durations = {"fetch": 1}
        if getattr(player, "interaction_progress", 0) == 0:
            player.interaction_progress = durations["fetch"]
            return player.interaction_progress

        player.interaction_progress -= 1
        if player.interaction_progress < 0:
            player.interaction_progress = 0

        if player.interaction_progress == 0:
            self.perform(player)
            return 0

        return player.interaction_progress

    def perform(self, player):
        if player.itemWanted:
            ingredient_obj = Ingredient(player.itemWanted, "raw")
            player.grab(ingredient_obj)
            print(f"Fridge gave {ingredient_obj} to {player}.")
        # Fridge ne stocke rien
        self.itemHeld = None
