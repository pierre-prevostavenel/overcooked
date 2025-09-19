import pygame
import random

class Player:
    def __init__(self, x=0, y=0, tile_size=50):
        self.map_width = 10
        self.tile_size = tile_size
        
        # Position en index 1D dans la grille
        self.position = y * self.map_width + x
        self.manual_control = False

        # Chargement de l'image et création du rect pour le dessin
        try:
            # Charge l'image et la met à l'échelle de la tuile
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        except pygame.error:
            # Si l'image n'est pas trouvée, crée une surface rouge en remplacement
            print("Attention : L'image 'assets/player.png' n'a pas été trouvée.")
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 0)) # Rouge

        # Crée le rectangle pour la position en pixels
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size, y * tile_size)

    def update(self):
        """Met à jour la position du joueur (logique de grille)."""
        # Si le joueur est contrôlé par les touches
        if self.manual_control:
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_z] and self.position >= self.map_width:
                self.position -= self.map_width
                moved = True
            elif keys[pygame.K_s] and self.position < self.map_width * (self.map_width - 1):
                self.position += self.map_width
                moved = True
            elif keys[pygame.K_q] and self.position % self.map_width != 0:
                self.position -= 1
                moved = True
            elif keys[pygame.K_d] and self.position % self.map_width != self.map_width - 1:
                self.position += 1
                moved = True
        else:
            # Mouvement automatique aléatoire
            mouvements_possibles = []
            
            # haut
            if self.position >= self.map_width:
                mouvements_possibles.append(-self.map_width)
            # bas
            if self.position < self.map_width * (self.map_width - 1):
                mouvements_possibles.append(self.map_width)
            # gauche
            if self.position % self.map_width != 0:
                mouvements_possibles.append(-1)
            # droite
            if self.position % self.map_width != self.map_width - 1:
                mouvements_possibles.append(1)

            if mouvements_possibles:
                mouvement = random.choice(mouvements_possibles)
                self.position += mouvement
        
        # Met à jour la position en pixels (le rect) à partir de la position en grille
        current_col = self.position % self.map_width
        current_row = self.position // self.map_width
        self.rect.topleft = (current_col * self.tile_size, current_row * self.tile_size)

        print(f"Position du joueur : {current_col}, {current_row}")

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft)