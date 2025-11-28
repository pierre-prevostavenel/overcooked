import os
import pygame
from pygame.sprite import LayeredUpdates
from random import randint

from player.Player import Player
from maps.Maps import Maps
from food.Order import Order
from food.Dish import Dish
from food.Ingredient import Ingredient
from utils.GameState import GameState
from utils.Blackboard import Blackboard


class Game:
    score = 0

    def __init__(self, screen_width=720, screen_height=720):
        pygame.init()

        json_path = os.path.join(os.path.dirname(__file__), "food", "food.json")
        Ingredient.init(json_path)
        Ingredient.init(json_path)

        self.blackboard = Blackboard()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("OverCooked")
        
        # Init dishes after display init because they load images
        Dish.init(json_path)
        
        self.clock = pygame.time.Clock()

        self.tile_size = screen_width // 10
        self.maps = Maps(tile_size=self.tile_size)
        self.all_sprites = pygame.sprite.LayeredUpdates()

        for row in self.maps.grid:
            for tile in row:
                self.all_sprites.add(tile)

        self.gameState = GameState()
        self.font = pygame.font.SysFont("arial", 20)
        self.hud_font = pygame.font.SysFont("arial", 18)

        self.orders = [Order(60)]
        self.blackboard.announce(f"Commande initiale : « {self.orders[0].desired_dish.name} ».")

        self.players = [
            Player(json_path, agent_id=1, start=(1, 2), tile_size=self.tile_size, map_size=(self.maps.width, self.maps.height), blackboard=self.blackboard, color=(52, 152, 219)),
            Player(json_path, agent_id=2, start=(8, 2), tile_size=self.tile_size, map_size=(self.maps.width, self.maps.height), blackboard=self.blackboard, color=(231, 76, 60)),
        ]
        for agent in self.players:
            self.all_sprites.add(agent)

        self.running = True
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.players[0].manual_control = not self.players[0].manual_control

                controller = self.players[0]
                if controller.manual_control:
                    target_x, target_y = controller.x, controller.y
                    if event.key == pygame.K_z and controller.y > 0:
                        target_y -= 1
                    elif event.key == pygame.K_s and controller.y < self.maps.height - 1:
                        target_y += 1
                    elif event.key == pygame.K_q and controller.x > 0:
                        target_x -= 1
                    elif event.key == pygame.K_d and controller.x < self.maps.width - 1:
                        target_x += 1

                    if (target_x, target_y) != (controller.x, controller.y):
                        occupied = any(
                            (agent.x, agent.y) == (target_x, target_y)
                            for agent in self.players
                            if agent is not controller
                        )
                        if not occupied:
                            controller.x, controller.y = target_x, target_y
                            controller.position = controller.y * self.maps.width + controller.x
                            controller.rect.topleft = (controller.x * self.tile_size, controller.y * self.tile_size)

    def update(self):
        self.all_sprites.update(self)
        self.blackboard.update_visuals()

    def get_orders(self):
        return self.orders

    def get_maps(self):
        return self.maps

    def accept_plate(self, plate, order):
        if order not in self.orders:
            return False
        success = plate.verify(order.desired_dish)
        self.orders.remove(order)
        if success:
            self.score += 1
            self.gameState.complete_order()
            self.blackboard.announce(f"Commande « {order.desired_dish.name} » servie !")
        else:
            self.gameState.fail_order()
            self.blackboard.announce(f"Commande « {order.desired_dish.name} » refusée.")
        self.blackboard.finalize_order(order)
        return success

    def updateOrders(self):
        self.blackboard.drop_missing_orders(self.orders)
        for o in self.orders[:]:
            if not o.update():
                self.orders.remove(o)
                self.gameState.fail_order()
                self.blackboard.finalize_order(o)
                self.blackboard.announce(f"Commande « {o.desired_dish.name} » a expiré.")

        if randint(1, 600) <= 1:
            order = Order(60)
            self.orders.append(order)
            self.blackboard.announce(f"Nouvelle commande : « {order.desired_dish.name} ».")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        for agent in self.players:
            agent.draw(self.screen)

        Order.draw_orders(self.screen, self.orders, self.font)

        score_text = self.hud_font.render(f"Score: {self.score}", True, (255, 255, 255))
        stats_text = self.hud_font.render(
            f"Succès: {self.gameState.completed_orders} | Échecs: {self.gameState.failed_orders}",
            True,
            (200, 200, 200),
        )
        self.screen.blit(score_text, (10, self.screen_height - 55))
        self.screen.blit(stats_text, (10, self.screen_height - 30))
        self.screen.blit(score_text, (10, self.screen_height - 55))
        self.screen.blit(stats_text, (10, self.screen_height - 30))
        
        # Draw plated ingredients and visual effects
        self.blackboard.draw_plated_ingredients(self.screen)
        self.blackboard.draw_visuals(self.screen)
        
        self.blackboard.draw(self.screen, self.hud_font, self.screen_width - 260, 10)

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
