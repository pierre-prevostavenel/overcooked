### main.py :
import pygame
from pygame.sprite import LayeredUpdates
from Player import Player
from Maps import Maps
from random import randint
from Client import Client
from Order import Order
from GameState import GameState

class Game:
    def __init__(self, screen_width=720, screen_height=720):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("OverCooked")
        self.clock = pygame.time.Clock()

        self.tile_size = screen_width // 10
        self.maps = Maps(tile_size=self.tile_size)
        self.current_level_index = 0
        self.all_sprites = self.maps.get_level(self.current_level_index)

        self.gameState = GameState()

        self.orders = []

        self.player = Player(self.maps,tile_size=self.tile_size)
        self.all_sprites.add(self.player)

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

                # AJOUT : Gérer le déplacement si le mode manuel est actif
                if self.player.manual_control:
                    moved = False
                    if event.key == pygame.K_z and self.player.position >= self.player.map_width:
                        self.player.position -= self.player.map_width
                        moved = True
                    elif event.key == pygame.K_s and self.player.position < self.player.map_width * (self.player.map_width - 1):
                        self.player.position += self.player.map_width
                        moved = True
                    elif event.key == pygame.K_q and self.player.position % self.player.map_width != 0:
                        self.player.position -= 1
                        moved = True
                    elif event.key == pygame.K_d and self.player.position % self.player.map_width != self.player.map_width - 1:
                        self.player.position += 1
                        moved = True
                    
                    # Si le joueur a bougé, on met à jour sa position graphique (le rect)
                    if moved:
                        current_col = self.player.position % self.player.map_width
                        current_row = self.player.position // self.player.map_width
                        self.player.rect.topleft = (current_col * self.player.tile_size, current_row * self.player.tile_size)
                        print(f"Position du joueur : {current_col}, {current_row}")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.prev_button.collidepoint(mouse_pos):
                    self.previous_level()
                elif self.next_button.collidepoint(mouse_pos):
                    self.next_level()

    def update(self):
        self.all_sprites.update()

    def updateOrders(self):
        for o in self.orders[:]:  
            if not o.update():
                self.orders.remove(o)
                self.gameState.fail_order()
                print("Commande raté :/ ! " + o.__str__())
                
        #TODO voir pour faire "scale" la difficultée
        if randint(1, 100) <= 1:
            order = Order(30) #possible de chager le temps restant pour une commande
            print("Nouvelle commandes ! " + order.__str__())
            self.orders.append(order)
            print(f"Total commande : {len(self.orders)}")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        pygame.draw.rect(self.screen, (100, 100, 255), self.prev_button)
        pygame.draw.rect(self.screen, (100, 100, 255), self.next_button)
        self.screen.blit(self.font.render("Précédent", True, (255,255,255)), (self.prev_button.x+10, self.prev_button.y+8))
        self.screen.blit(self.font.render("Suivant", True, (255,255,255)), (self.next_button.x+20, self.next_button.y+8))

        pygame.display.flip()

    def next_level(self):
        if self.current_level_index + 1 < self.maps.num_levels():
            self.current_level_index += 1
            self.all_sprites = self.maps.get_level(self.current_level_index)
            self.all_sprites.add(self.player)

    def previous_level(self):
        if self.current_level_index - 1 >= 0:
            self.current_level_index -= 1
            self.all_sprites = self.maps.get_level(self.current_level_index)
            self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.handle_events()
            self.updateOrders()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()