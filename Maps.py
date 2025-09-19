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
        map1 = [["whitefloor"]*10 for _ in range(10)]
        map1[2][2] = "blackfloor"
        map1[4][1] = "gas_station"

        # Exemple Map 2
        map2 = [["blackfloor"]*10 for _ in range(10)]
        map2[1][1] = "whitefloor"
        map2[3][1] = "gas_station"

        self.levels.append(map1)
        self.levels.append(map2)

    def get_level(self, index, add_random_tiles=False, num_random=5):
        """Retourne la map demandée sous forme de LayeredUpdates de tiles."""
        grid_data = self.levels[index]
        tiles = LayeredUpdates()
        for r, row in enumerate(grid_data):
            for c, tile_type in enumerate(row):
                tile = Tile(r, c, tile_type, self.tile_size)
                tiles.add(tile)

        if add_random_tiles:
            from random import choice, randint
            positions = set()
            while len(positions) < num_random:
                r = randint(0, len(grid_data)-1)
                c = randint(0, len(grid_data[0])-1)
                if (r,c) not in positions:
                    positions.add((r,c))
                    tile_type = choice(list(Tile.TILE_IMAGES.keys()))
                    tiles.add(Tile(r, c, tile_type, self.tile_size))

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
