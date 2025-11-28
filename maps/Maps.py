# Maps.py
from maps.Tile import Tile
from maps.Station import *

class Maps:
    """Grille unique construite directement avec Tiles et Stations."""
    def __init__(self, width=10, height=10, tile_size=50):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid = [[Tile(r, c, "floor", tile_size) for c in range(width)] for r in range(height)]
        self._build_map()

    def _build_map(self):
        """Map labyrinthe : Workbench = mur, floor = chemin, Fridge = objectif"""
        layout = [
            ["wall", "workbench2", "workbench2", "workbench2", "workbench2", "workbench2", "workbench2", "workbench2", "workbench2", "wall"],
            ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
            ["wall", "floor", "floor", "table", "floor", "floor", "floor", "floor", "floor", "wall"],
            ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
            ["wall", "trash1", "floor", "floor", "floor", "floor", "floor", "floor","floor", "wall"],
            ["wall", "workbench", "floor", "floor", "floor", "floor", "floor", "floor", "white_sink", "wall"],
            ["wall", "workbench","floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
            ["wall", "workbench", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
            ["wall", "workbench", "floor", "trash1", "coffee_machine", "floor", "fridge", "floor", "oven", "wall"],
            ["wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall"],
        ]

        for r in range(self.height):
            for c in range(self.width):
                cell = layout[r][c]
                if cell == "floor":
                    self.grid[r][c] = Tile(r, c, "floor", self.tile_size)
                elif cell == "workbench":
                    self.grid[r][c] = Workbench(r, c, self.tile_size)
                elif cell == "fridge":
                    self.grid[r][c] = Fridge(r, c, self.tile_size)
                elif cell == "oven":
                    self.grid[r][c] = Oven(r, c, self.tile_size)
                elif cell == "white_sink":
                    self.grid[r][c] = WhiteSink(r, c, self.tile_size)
                elif cell == "coffee_machine":
                    self.grid[r][c] = CoffeeMachine(r, c, self.tile_size)
                else:
                    self.grid[r][c] = Tile(r, c, cell, self.tile_size)
