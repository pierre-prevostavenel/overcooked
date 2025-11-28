import os
import sys
import argparse
import pygame
import random

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

    def __init__(self, screen_width=720, screen_height=720, simulation=True, max_steps=None, nb_agents=2):
        self.simulation = simulation
        self.max_steps = max_steps
        self.current_step = 0
        if self.simulation:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
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

        colors = [
            (57, 255, 20),    
            (0, 255, 255),    
            (255, 0, 255),    
            (255, 255, 0),    
            (255, 105, 180),  
            (0, 191, 255),    
            (255, 87, 51),    
            (186, 85, 211),   
            (0, 255, 127),    
        ]

        all_tiles = [
            (x, y)
            for x in range(self.maps.width)
            for y in range(self.maps.height)
            if self.maps.grid[y][x].tile_type == "floor"
        ]

        random.shuffle(all_tiles)
        tiles = all_tiles[:nb_agents]

        self.players = []   
        for i in range(nb_agents):
            self.players.append(
                Player(json_path, agent_id=i+1, start=tiles[i], tile_size=self.tile_size, map_size=(self.maps.width, self.maps.height), blackboard=self.blackboard, color=colors[i]))


        for agent in self.players:
            self.all_sprites.add(agent)

        self.running = True
        self.score = 0
        self.failed_orders = 0

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
            self.failed_orders += 1
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
            order = Order(30)
            self.orders.append(order)
            self.blackboard.announce(f"Nouvelle commande : « {order.desired_dish.name} ».")

    def draw(self):
        if self.simulation:
            return
        
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
            if not self.simulation:
                self.clock.tick(120)
            
            if self.max_steps:
                self.current_step += 1
                if self.current_step >= self.max_steps:
                    self.running = False

        pygame.quit()
        return (self.score, self.failed_orders)

def run_games(nb_games,max_step, nb_agents):
    scores = []
    failed_orders = []
    for i in range(nb_games):
        sys.stdout = sys.__stdout__
        print(f"\nGame {i+1}/{nb_games}")
        sys.stdout = open(os.devnull, 'w')

        game = Game(simulation=args.simulation, max_steps=max_step, nb_agents=nb_agents)
        
        score, failed = game.run()
        scores.append(score)
        failed_orders.append(failed)

        if args.num_games > 1:
            print(f"Game {i+1}/{args.num_games} finished. Score: {score}")
    return scores, failed_orders


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Overcooked Simulation")
    parser.add_argument("--simulation", action="store_true", help="launch a fast simulation")
    parser.add_argument("--num-games", type=int, default=0, help="Number of games to run (default: 1)")
    parser.add_argument("--max-steps", type=int, default=2000, help="Maximum steps per game (default: 2000)")
    parser.add_argument("--nb-agents", type=int, default=2, help="Number of agents (default: 2)")
    parser.add_argument("--output", type=str, default="results", help="Output file for results graph (default: results)")
    args = parser.parse_args()
    
    if not args.simulation and args.num_games == 0:
        game = Game(simulation=False, nb_agents=args.nb_agents)
        game.run()

    scores, failed_orders = run_games(args.num_games, args.max_steps, args.nb_agents)

    if args.num_games > 0:
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)

        avg_failed_orders = sum(failed_orders) / len(failed_orders)
        min_failed_orders = min(failed_orders)
        max_failed_orders = max(failed_orders)

        sys.stdout = sys.__stdout__
        print(f"\n--- Statistics ({args.num_games} games) ---")
        print(f"Average Score: {avg_score:.2f}")
        print(f"Min Score: {min_score}")
        print(f"Max Score: {max_score}")

        print(f"Average Failed Orders: {avg_failed_orders:.2f}")
        print(f"Min Failed Orders: {min_failed_orders}")
        print(f"Max Failed Orders: {max_failed_orders}")

        # Generate Matplotlib Graph
        try:
            import matplotlib.pyplot as plt
            from collections import Counter
            
            score_counts = Counter(scores)
            labels = sorted(score_counts.keys())
            data = [score_counts[l] for l in labels]

            plt.figure(figsize=(10, 6))
            plt.bar(labels, data, color='skyblue', edgecolor='black')
            plt.xlabel('Score')
            plt.ylabel('Frequency')
            plt.title(f'Simulation Results ({args.num_games} games, {args.nb_agents} agents) - max steps: {args.max_steps}')
            plt.xticks(labels)
            plt.grid(axis='y', alpha=0.75)
            
            file_out_name= args.output+"_"+str(args.nb_agents)+"_agents.svg"
            plt.savefig(file_out_name)
            print(f"\nGraph saved to {file_out_name}")

            failed_orders_counts = Counter(failed_orders)
            labels = sorted(failed_orders_counts.keys())
            data = [failed_orders_counts[l] for l in labels]

            plt.figure(figsize=(10, 6))
            plt.bar(labels, data, color='skyblue', edgecolor='black')
            plt.xlabel('Failed Orders')
            plt.ylabel('Frequency')
            plt.title(f'Simulation Results ({args.num_games} games, {args.nb_agents} agents) - max steps: {args.max_steps}')
            plt.xticks(labels)
            plt.grid(axis='y', alpha=0.75)
            
            file_out_name= args.output+"_"+str(args.nb_agents)+"_agents_failed_orders.svg"
            plt.savefig(file_out_name)
            print(f"\nGraph saved to {file_out_name}")

        except ImportError:
            print("\n[Error] matplotlib is not installed. Cannot generate graph.")
        except Exception as e:
            print(f"\n[Error] Failed to generate graph: {e}")
