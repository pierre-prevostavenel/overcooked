import pygame

from MySprite import MySprite


class Item(MySprite):
    count = 0  # variable de classe

    def __init__(self, name, image_path, x, y):
        super().__init__()
        Item.count += 1
        self.id = f"Item{Item.count}"
        self.name = name
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

