# Tile.py
import pygame
from utils.MySprite import MySprite

class Tile(MySprite):
    TILE_IMAGES = {
        "whitefloor": "assets/white_tile.png",
        "blackfloor": "assets/black_tile.png",
        "oven": "assets/gas.png",
        "floor": "assets/floor.png",
        "fridge": "assets/fridge.png",
        "workbench": "assets/workbench.png",
        "workbench2": "assets/workbench2.png",
        "table": "assets/table.png",
        "trash1": "assets/trash1.png",
        "trash2": "assets/trash2.png",
        "trash3": "assets/trash3.png",
        "player": "assets/player.png",
    }

    def __init__(self, row, col, tile_type="whitefloor", tile_size=50):
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.tile_size = tile_size
        rect = (col * tile_size, row * tile_size, tile_size, tile_size)
        image_path = self.TILE_IMAGES.get(tile_type, None)
        super().__init__(rect, image_path)
