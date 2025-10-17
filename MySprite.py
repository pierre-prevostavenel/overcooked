from pygame.sprite import Sprite
import pygame
import os

class MySprite(Sprite):
    def __init__(self, rect, image_path="./assets/player.png", fallback_color=(255, 0, 0), layer=0):
        super().__init__()
        self._layer = layer
        self.rect = pygame.Rect(rect)
        self.image = self.load_image(image_path, fallback_color)

    def load_image(self, image_path, fallback_color):
        if image_path and os.path.isfile(image_path):
            try:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, self.rect.size)
                return image
            except pygame.error:
                print(f"[Error] Failed to load image: {image_path}")
        # Fallback: solid color surface
        surface = pygame.Surface(self.rect.size)
        surface.fill(fallback_color)
        return surface
    
def __str__(self):
    return (f"<MySprite rect={self.rect} "
            f"layer={self._layer} "
            f"image_path={'None' if not hasattr(self, 'image') else getattr(self, 'image_path', 'Unknown')} "
            f"fallback_color={self.fallback_color if hasattr(self, 'fallback_color') else 'N/A'}>")
