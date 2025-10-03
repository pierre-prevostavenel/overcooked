import pygame
from pygame.sprite import LayeredUpdates
from Tile import Tile

class Maps:
    """Classe qui contient toutes les maps et gère l'accès par niveau."""
    def __init__(self, tile_size=72):
        self.tile_size = tile_size
        self.levels = []
        self._load_maps()

    def _load_maps(self):
        """Charge ou définit toutes les maps ici."""
        # Exemple Map 1
        map1 = [
            ["workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "gas1",      "floor",     "floor",     "floor",     "gas2",      "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "workbench",  "floor",    "floor",     "floor","workbench",  "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "fridge",    "floor",     "floor",     "floor",     "floor",     "floor",     "white_sink", "workbench"],
            ["workbench", "floor",     "workbench",  "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "gas3",      "floor",     "floor",     "floor",     "floor",     "trash1",    "trash2",    "workbench"],
            ["workbench", "floor",     "workbench4", "floor",     "floor",   "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench"],
        ]

        # Exemple Map 2
        map2 = [["blackfloor"]*10 for _ in range(10)]
        map2[1][1] = "whitefloor"
        map2[3][1] = "gas_station"

        self.levels.append(map1)
        self.levels.append(map2)

    def get_level(self, index):
        """Retourne la map demandée sous forme de LayeredUpdates de tiles."""
        grid_data = self.levels[index]
        tiles = LayeredUpdates()
        for r, row in enumerate(grid_data):
            for c, tile_type in enumerate(row):
                # Toujours créer un floor en dessous
                if tile_type != "floor" and tile_type != "blackfloor":
                    floor_tile = Tile(r, c, "floor", self.tile_size)
                    tiles.add(floor_tile, layer=0)
                    tile = Tile(r, c, tile_type, self.tile_size)
                    tiles.add(tile, layer=1)
                else:
                    tile = Tile(r, c, tile_type, self.tile_size)
                    tiles.add(tile, layer=0)

        return tiles


    def num_levels(self):
        return len(self.levels)
    
    def get_nearest(self, posx, posy, tile_type, level_index=None):
        """
        Retourne la tile du type 'tile_type' la plus proche de (posx, posy).
        level_index : si None, prend la map actuelle.
        """
        if level_index is None:
            level_index = self.current_level_index if hasattr(self, 'current_level_index') else 0

        tiles_layer = self.get_level(level_index)  # LayeredUpdates
        nearest_tile = None
        min_dist = float('inf')

        for tile in tiles_layer:
            if getattr(tile, "tile_type", None) == tile_type:
                # Calcul de la distance euclidienne entre le centre de la tile et posx, posy
                tile_center = tile.rect.center
                dist = math.hypot(tile_center[0] - posx, tile_center[1] - posy)
                if dist < min_dist:
                    min_dist = dist
                    nearest_tile = tile

        return nearest_tile
