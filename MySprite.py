from pygame.sprite import Sprite
import pygame
import os
class MySprite(Sprite):
    def __init__(self, rect, image_path=None, fallback_color=(255, 0, 0), layer=0):
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