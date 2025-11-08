# Maps.py
from maps.Tile import Tile
from maps.Station import Workbench, Fridge, GasStation

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
            ["Workbench","Workbench","Workbench","Workbench","Workbench","Workbench","Workbench","Workbench","Workbench","Workbench"],
            ["Workbench","floor",    "floor",    "floor",    "Workbench","floor",    "floor",    "floor",    "floor",    "Workbench"],
            ["Workbench","floor",    "Workbench","floor",    "Workbench","floor",    "Workbench","Workbench","floor",    "Workbench"],
            ["Workbench","floor",    "Workbench","floor",    "floor",    "floor",    "Workbench","floor",    "floor",    "Workbench"],
            ["Workbench","floor",    "Workbench","Workbench","Workbench","floor",    "Workbench","floor",    "Workbench","Workbench"],
            ["Workbench","floor",    "floor",    "floor",    "Workbench","gas_station",    "Workbench","floor",    "floor",    "Workbench"],
            ["Workbench","Workbench","Workbench","floor",    "Workbench","floor",    "Workbench","Workbench","floor",    "Workbench"],
            ["Workbench","floor",    "floor",    "floor",    "floor",    "floor",    "floor",    "Workbench","floor",    "Workbench"],
            ["Workbench","floor",    "Workben0ch","Workbench","Workbench","Workbench","floor",    "Workbench","floor",    "Workbench"],
            ["Workbench","floor",    "floor",    "floor",    "floor",    "floor",    "floor",    "floor",    "Fridge",   "Workbench"]
        ]

        for r in range(self.height):
            for c in range(self.width):
                cell = layout[r][c]
                if cell == "floor":
                    self.grid[r][c] = Tile(r, c, "floor", self.tile_size)
                elif cell == "Workbench":
                    self.grid[r][c] = Workbench(r, c, self.tile_size)
                elif cell == "Fridge":
                    self.grid[r][c] = Fridge(r, c, self.tile_size)
                elif cell == "gas_station":
                    self.grid[r][c] = GasStation(r, c, self.tile_size)
