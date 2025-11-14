import pygame
import sys
from pygame.sprite import LayeredUpdates
from player.Player import Player
from maps.Maps import Maps
from random import randint
from food.Order import Order
from food.Dish import *
from food.Ingredient import *
from utils.GameState import GameState

class Game:
    score=0
    def __init__(self, screen_width=720, screen_height=720):

        pygame.init()

        json_path = os.path.join(os.path.dirname(__file__)+"/food", "food.json")
        Ingredient.init(json_path)
        Dish.init(json_path)
        

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
                #print(f"Added tile at ({tile.row}, {tile.col}) of type '{tile.tile_type}'")

        self.gameState = GameState()



        self.orders = [Order(60)]

        self.player = Player(json_path, tile_size=self.tile_size)
        self.all_sprites.add(self.player)

        self.running = True

        self.score = 0

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
        self.all_sprites.update(self)

    def get_orders(self):
        return self.orders
    
    def get_maps(self):
        return self.maps

    def accept_plate(self,plate):
        print("Resultat accept plate : ", plate.verify(self.orders[0].desired_dish))
        if(plate.verify(self.orders[0].desired_dish)):
            self.score +=1 
            print("COMMANDE REUSSIE ! score actuel : ", self.score)
            self.orders.remove(self.orders[0])
            return True
        print("Commande ratée :/ ! " + self.orders[0].__str__(), "plate ", plate)
        self.orders.remove(self.orders[0])
        return False

    def updateOrders(self):
        for o in self.orders[:]:
            if not o.update():
                self.orders.remove(o)
                self.gameState.fail_order()
                print("Commande ratée ! L'agent a perdu " + o.__str__())
                sys.exit("Commande ratée, l'agent a perdu.")
                
        #TODO voir pour faire "scale" la difficulté
        if randint(1, 600) <= 1: #en moyenne 1 commande toute les 10 secondes
            order = Order(60) #possible de changer le temps restant pour une commande
            #print("Nouvelle commandes ! " + order.__str__())
            self.orders.append(order)
            #print(f"Total commande : {len(self.orders)}")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.draw(self.screen)

        # Changement de map (plus utilisé)
        # self.screen.blit(self.font.render("Précédent", True, (255,255,255)), (self.prev_button.x+10, self.prev_button.y+8))
        # self.screen.blit(self.font.render("Suivant", True, (255,255,255)), (self.next_button.x+20, self.next_button.y+8))
        Order.draw_orders(self.screen, self.orders, pygame.font.SysFont("arial", 20))
        pygame.display.flip()

    def run(self):
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
