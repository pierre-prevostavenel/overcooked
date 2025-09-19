import pygame
from pygame.sprite import LayeredUpdates
import random
from Player import Player
from Tile import Tile

class Game:
    def __init__(self, screen_width=720, screen_height=720, rows=10, cols=10, num_tiles=5):
        # Pygame
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("OverCooked")
        self.clock = pygame.time.Clock()

        # Grille et tuiles
        self.rows = rows
        self.cols = cols
        self.tile_size = screen_width // cols
        self.num_tiles = num_tiles

        # Joueur
        self.player = Player()

        # Sprites
        self.all_sprites = LayeredUpdates()
        self._add_random_tiles()

        self.running = True

    def _add_random_tiles(self):
        """Ajoute des tiles aléatoires à la map sans duplication de position."""
        positions_prisees = set()
        while len(positions_prisees) < self.num_tiles:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in positions_prisees:
                positions_prisees.add((row, col))
                tile_type = random.choice(list(Tile.TILE_IMAGES.keys()))
                tile = Tile(row, col, tile_type, self.tile_size)
                self.all_sprites.add(tile)

    def handle_events(self):
        """Gestion des événements Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Inverse le contrôle manuel du joueur
                    self.player.manual_control = not self.player.manual_control

    def update(self):
        """Met à jour tous les sprites et le joueur."""
        self.all_sprites.update()
        self.player.update()

    def draw(self):
        """Dessine tous les éléments à l'écran."""
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
