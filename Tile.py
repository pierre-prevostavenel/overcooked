import pygame

class Tile:
    # Load sprites once as class variables
    FLOOR_IMG = pygame.image.load("floor.png").convert_alpha()
    COUNTER_IMG = pygame.image.load("counter.png").convert_alpha()

    def __init__(self, row, col, tile_type="floor"):
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.occupied = False
        self.sprite = self.get_sprite_for_type(tile_type)

    def get_sprite_for_type(self, tile_type):
        if tile_type == "floor":
            return Tile.FLOOR_IMG
        elif tile_type == "counter":
            return Tile.COUNTER_IMG
        else:
            return None

    def set_type(self, tile_type):
        self.tile_type = tile_type
        self.sprite = self.get_sprite_for_type(tile_type)

    def position(self, tile_size):
        return (self.col * tile_size, self.row * tile_size)

    def draw(self, surface, tile_size):
        x, y = self.position(tile_size)
        if self.sprite:
            surface.blit(self.sprite, (x, y))
        else:
            pygame.draw.rect(surface, (200,200,200), (x, y, tile_size, tile_size))
            pygame.draw.rect(surface, (0,0,0), (x, y, tile_size, tile_size), 1)
