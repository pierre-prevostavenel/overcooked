import pygame
from MySprite import MySprite

# Dictionnaire pour mapper les types de tuiles vers des chemins d'images
TILE_IMAGES = {
    "whitefloor": "assets/white_tile.png",
    "blackfloor": "assets/black_tile.png",
    "gas_station": "assets/gas.png"
}

class Tile(MySprite):
    def __init__(self, row, col, tile_type="floor", tile_size=50):
        """
        row, col : position de la tuile dans la grille
        tile_type : type de la tuile ("floor", "counter", "wall", etc.)
        tile_size : taille de la tuile en pixels (carré)
        """
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.tile_size = tile_size

        # Calcule la position en pixels pour pygame.Rect
        rect = (col * tile_size, row * tile_size, tile_size, tile_size)

        # Choisit le chemin de l'image selon le type
        image_path = TILE_IMAGES.get(tile_type, None)

        # Appelle le constructeur de MySprite
        super().__init__(rect, image_path)

    def set_type(self, new_type):
        """Change le type de la tuile et met à jour l'image."""
        self.tile_type = new_type
        image_path = TILE_IMAGES.get(new_type, None)
        self.image = self.load_image(image_path, fallback_color=(200, 200, 200))

    def draw(self, surface, tile_size=None):
        """Dessine la tuile sur la surface donnée."""
        if tile_size:
            # Ajuste l'image si la taille de dessin change
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
            self.rect.size = (tile_size, tile_size)
        surface.blit(self.image, self.rect.topleft)
