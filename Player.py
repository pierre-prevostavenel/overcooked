### player.py :
import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, x=0, y=0, tile_size=50):
        super().__init__()
        self.maps = maps
        self.map_width = 10
        self.tile_size = tile_size
        self.x = x
        self.y = y
        self.position = y * self.map_width + x
        self.manual_control = False
        self.path = []
        self.move_timer = 0
        self.state = "IDLE"

        try:
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        except pygame.error:
            print("Attention : L'image 'assets/player.png' n'a pas été trouvée.")
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size, y * tile_size)

    def update(self):
        # Toutes les 1/2s (30 ticks)
        self.move_timer += 1
        if self.move_timer == 30:
            self.move_timer = 0
        if self.move_timer == 0:
            match self.state:
                case "WALKING":
                    try:
                        self.x, self.y = self.path[0]
                        self.position = self.x*self.map_width+self.y
                        self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                        if len(self.path) == 2:  # On s'arrête quand on est à côté de la case visée
                            self.path = []
                            self.state = "IDLE"
                        else:
                            self.path = self.path[1:]
                    except TypeError:
                        print(f"self.path: {self.path}")
                case "IDLE":
                    print("idle player")
        
    def go_to(self, target: str):
        print(f"Appel de go_to {target}")
        self.state = "WALKING"
        self.path = self.maps.get_path(self.x, self.y, target, 0)
        print(f"chemin: {self.path}")

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft)