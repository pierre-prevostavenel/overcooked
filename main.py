import pygame
from pygame.sprite import LayeredUpdates
from Player import Player
from Maps import Maps

class Game:
    def __init__(self, screen_width=720, screen_height=720):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("OverCooked")
        self.clock = pygame.time.Clock()

        # Maps
        self.maps = Maps(tile_size=screen_width // 10)
        self.current_level_index = 0
        self.all_sprites = self.maps.get_level(self.current_level_index, add_random_tiles=True)

        # Joueur
        self.player = Player()
        self.all_sprites.add(self.player)

        # Boutons
        self.button_width = 120
        self.button_height = 40
        self.prev_button = pygame.Rect(10, screen_height - 50, self.button_width, self.button_height)
        self.next_button = pygame.Rect(screen_width - 130, screen_height - 50, self.button_width, self.button_height)
        self.font = pygame.font.SysFont(None, 30)

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.manual_control = not self.player.manual_control

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.prev_button.collidepoint(mouse_pos):
                    self.previous_level()
                elif self.next_button.collidepoint(mouse_pos):
                    self.next_level()

    def update(self):
        self.all_sprites.update()
        self.player.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        # Dessiner boutons
        pygame.draw.rect(self.screen, (100, 100, 255), self.prev_button)
        pygame.draw.rect(self.screen, (100, 100, 255), self.next_button)
        self.screen.blit(self.font.render("Précédent", True, (255,255,255)), (self.prev_button.x+10, self.prev_button.y+8))
        self.screen.blit(self.font.render("Suivant", True, (255,255,255)), (self.next_button.x+20, self.next_button.y+8))

        pygame.display.flip()

    def next_level(self):
        if self.current_level_index + 1 < self.maps.num_levels():
            self.current_level_index += 1
            self.all_sprites = self.maps.get_level(self.current_level_index, add_random_tiles=True)
            self.all_sprites.add(self.player)

    def previous_level(self):
        if self.current_level_index - 1 >= 0:
            self.current_level_index -= 1
            self.all_sprites = self.maps.get_level(self.current_level_index, add_random_tiles=True)
            self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
