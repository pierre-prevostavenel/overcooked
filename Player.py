import pygame
import random

class Player:
    def __init__(self, x=0, y=0):
        self.largeur_map = 10
        self.position = x * self.largeur_map + y

    def update(self, manual_control=True):
        # Si le joueur est contrôlé par les touches
        if manual_control:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_z] and self.position >= self.largeur_map:
                self.position -= self.largeur_map

            if keys[pygame.K_s] and self.position < self.largeur_map * (self.largeur_map - 1):
                self.position += self.largeur_map

            if keys[pygame.K_q] and self.position % self.largeur_map != 0:
                self.position -= 1

            if keys[pygame.K_d] and self.position % self.largeur_map != self.largeur_map - 1:
                self.position += 1
        else:
            mouvements_possibles = []
            
            # haut
            if self.position >= self.largeur_map:
                mouvements_possibles.append(-self.largeur_map)

            # bas
            if self.position < self.largeur_map * (self.largeur_map - 1):
                mouvements_possibles.append(self.largeur_map)

            # gauche
            if self.position % self.largeur_map != 0:
                mouvements_possibles.append(-1)

            # droite
            if self.position % self.largeur_map != self.largeur_map - 1:
                mouvements_possibles.append(1)

            # On choisit un mouvement uniquement parmi ceux qui sont valides
            if mouvements_possibles:
                mouvement = random.choice(mouvements_possibles)
                self.position += mouvement

