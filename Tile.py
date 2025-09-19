import pygame
from MySprite import MySprite

class Tile(MySprite):
    TILE_IMAGES = {
        "whitefloor": "assets/white_tile.png",
        "blackfloor": "assets/black_tile.png",
        "gas_station": "assets/gas.png"
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

    
        