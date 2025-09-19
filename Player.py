import pygame
import random

class Player:
    def __init__(self, x=0, y=0):
        self.map_width = 10
        self.position = x * self.map_width + y
        self.manual_control = False

    def update(self):
        # Si le joueur est contrôlé par les touches
        if self.manual_control:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_z] and self.position >= self.map_width:
                self.position -= self.map_width

            if keys[pygame.K_s] and self.position < self.map_width * (self.map_width - 1):
                self.position += self.map_width

            if keys[pygame.K_q] and self.position % self.map_width != 0:
                self.position -= 1

            if keys[pygame.K_d] and self.position % self.map_width != self.map_width - 1:
                self.position += 1
        else:
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

            # On choisit un mouvement uniquement parmi ceux qui sont valides
            if mouvements_possibles:
                mouvement = random.choice(mouvements_possibles)
                self.position += mouvement
        print(f"Position du joueur : {self.position%self.map_width}, {self.position // self.map_width}")
