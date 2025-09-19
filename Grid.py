import Tile

class Grid:
    def __init__(self, rows, cols, default_type="floor"):
        self.rows = rows
        self.cols = cols
        # Create a 2D grid of Tile objects
        self.tiles = [[Tile.Tile(r, c, default_type) for c in range(cols)] for r in range(rows)]

    def get_tile(self, row, col):
        return self.tiles[row][col]

    def set_tile_type(self, row, col, tile_type):
        self.tiles[row][col].tile_type = tile_type