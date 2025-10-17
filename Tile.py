import pygame
from MySprite import MySprite

class Tile(MySprite):
    TILE_IMAGES = {
        "whitefloor": "assets/white_tile.png",
        "blackfloor": "assets/black_tile.png",
        "oven": "assets/gas.png",
        "floor": "assets/floor.png",
        "white_sink": "assets/white_sink.png",
        "white_sink1": "assets/white_sink1.png",
        "table": "assets/table.png",
        "fridge": "assets/fridge.png",
        "gas1": "assets/gas1.png",
        "gas2": "assets/gas2.png",
        "gas3": "assets/gas3.png",
        "player": "assets/player.png",
        "trash1": "assets/trash1.png",
        "trash2": "assets/trash2.png",
        "trash3": "assets/trash3.png",
        "workbench": "assets/workbench.png",
        "workbench2": "assets/workbench2.png",
        "workbench3": "assets/workbench3.png",
        "workbench4": "assets/workbench4.png",
}

    def __init__(self, row, col, tile_type="whitefloor", tile_size=50):
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.tile_size = tile_size

        rect = (col * tile_size, row * tile_size, tile_size, tile_size)
        image_path = self.TILE_IMAGES.get(tile_type, None)
        super().__init__(rect, image_path)

    def set_type(self, new_type):
        self.tile_type = new_type
        image_path = self.TILE_IMAGES.get(new_type, None)
        self.image = self.load_image(image_path, fallback_color=(200, 200, 200))

    def draw(self, surface, tile_size=None):
        if tile_size:
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
            self.rect.size = (tile_size, tile_size)
        surface.blit(self.image, self.rect.topleft)

    
        