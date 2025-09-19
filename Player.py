### player.py :
import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        
        self.position = y * self.map_width + x
        self.manual_control = False

        self.move_cooldown = 0
        self.move_timer = 20

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
        """Met à jour la position du joueur (logique de grille)."""
        # Si le contrôle est manuel, le mouvement est géré par les événements KEYDOWN, donc on ne fait rien ici.
        if self.manual_control:
            return

        # ---- Le code ci-dessous ne s'exécute qu'en mode automatique ----
        self.move_cooldown += 1
        if self.move_cooldown < self.move_timer:
            return
        
        self.move_cooldown = 0
        moved = False

        # Mouvement automatique aléatoire (le bloc 'if self.manual_control' a été retiré)
        mouvements_possibles = []
        if self.position >= self.map_width:
            mouvements_possibles.append(-self.map_width)
        if self.position < self.map_width * (self.map_width - 1):
            mouvements_possibles.append(self.map_width)
        if self.position % self.map_width != 0:
            mouvements_possibles.append(-1)
        if self.position % self.map_width != self.map_width - 1:
            mouvements_possibles.append(1)

        if mouvements_possibles:
            mouvement = random.choice(mouvements_possibles)
            self.position += mouvement
            moved = True
        
        if moved:
            current_col = self.position % self.map_width
            current_row = self.position // self.map_width
            self.rect.topleft = (current_col * self.tile_size, current_row * self.tile_size)
            print(f"Position du joueur : {current_col}, {current_row}")

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft)