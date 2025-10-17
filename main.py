import pygame
from Player import Player
from Maps import Maps
from random import randint
from Order import Order
from Dish import Dish
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
        self.all_sprites = pygame.sprite.LayeredUpdates()
        
        # ajouter toutes les tiles à all_sprites
        for row in self.maps.grid:
            for tile in row:
                self.all_sprites.add(tile)
                print(f"Added tile at ({tile.row}, {tile.col}) of type '{tile.tile_type}'")

        self.gameState = GameState()
        Dish.init()  # Dish s'occupe de charger le JSON
        self.orders = []

        self.player = Player(self.maps, tile_size=self.tile_size)
        self.all_sprites.add(self.player)
        self.player.set_order(self.orders)

        # Buttons si tu veux les garder
        self.font = pygame.font.SysFont("arial", 20)
        self.prev_button = pygame.Rect(10, screen_height - 40, 100, 30)
        self.next_button = pygame.Rect(screen_width - 110, screen_height - 40, 100, 30)

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.manual_control = not self.player.manual_control

                if self.player.manual_control:
                    moved = False
                    if event.key == pygame.K_z and self.player.y > 0:
                        self.player.y -= 1
                        moved = True
                    elif event.key == pygame.K_s and self.player.y < self.maps.height - 1:
                        self.player.y += 1
                        moved = True
                    elif event.key == pygame.K_q and self.player.x > 0:
                        self.player.x -= 1
                        moved = True
                    elif event.key == pygame.K_d and self.player.x < self.maps.width - 1:
                        self.player.x += 1
                        moved = True
                    
                    if moved:
                        self.player.position = self.player.y * self.maps.width + self.player.x
                        self.player.rect.topleft = (self.player.x * self.tile_size, self.player.y * self.tile_size)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # tu peux garder ces boutons ou les supprimer si inutile
                if self.prev_button.collidepoint(mouse_pos):
                    print("Bouton précédent désactivé")
                elif self.next_button.collidepoint(mouse_pos):
                    print("Bouton suivant désactivé")

    def update(self):
        self.all_sprites.update()

    def updateOrders(self):
        for o in self.orders[:]:
            if not o.update():
                self.orders.remove(o)
                self.gameState.fail_order()
                print("Commande ratée :/ " + str(o))
                
        if randint(1, 100) <= 1:
            order = Order(30)
            print("Nouvelle commande ! " + str(order))
            self.orders.append(order)
            print(f"Total commandes : {len(self.orders)}")
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.draw(self.screen)  # ← ici, draw() sera exécuté
        self.screen.blit(self.font.render("Précédent", True, (255,255,255)), (self.prev_button.x+10, self.prev_button.y+8))
        self.screen.blit(self.font.render("Suivant", True, (255,255,255)), (self.next_button.x+20, self.next_button.y+8))
        Order.draw_orders(self.screen, self.orders, self.font)
        pygame.display.flip()

    def run(self):
        # Par défaut, aller à la première station si nécessaire
        
        fridge_tile = self.maps.grid[9][8]
        oven_tile = self.maps.grid[5][5]
        self.player.targets = [fridge_tile, oven_tile]

        while self.running:
            self.handle_events()
            self.updateOrders()
            self.update()
            self.draw()
            self.clock.tick(120)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
