import heapq
from Maps import Node
import pygame
import json
from Ingredient import Ingredient
from Dish import Dish
from Action import *
import random
import os

from Station import Fridge, Station, Workbench
import Tile

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        self.maps = maps
        self.x = x
        self.y = y
        
        self.orders = []
        self.position = y * self.map_width + x
        self.manual_control = False

        # pré-calcul de plans pour réaliser les recettes
        self.transitions = {}
        self.init_transitions()
        self.move_cooldown = 0
        self.move_timer = 20
        self.interaction_progress = 0

        self.itemHeld : Item = None
        self.plans = [] 
        self.target = None  # cible actuelle
        self.path = None
        self.state = "IDLE"
        self.targets = []  # liste des cibles à suivre

        try:
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        except pygame.error:
            print("Attention : L'image 'assets/player.png' n'a pas été trouvée.")
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size, y * tile_size)
        

    def update(self):
        self.move_timer += 1
        self.move_timer %= 30
        if self.move_timer == 0:
            if len(self.plans) == 0:
                self.see()
            self.action()

        # aller vers la prochaine cible seulement si pas de chemin en cours et idle
        if self.targets and not self.path and self.state == "IDLE":
            self.go_to(self.targets[0])  # ne pop pas encore


    def init_transitions(self):
        json_path = os.path.join(os.path.dirname(__file__), "food.json")
        with open(json_path, "r") as f:
            data = json.load(f)

        for ing_data in data.get("ingredients", []):
            name = ing_data["name"]
            for state_data in ing_data.get("states", []):
                state = state_data["state"]
                src = (name, state)
                actions = state_data.get("actions", {})
                if not actions:
                    self.transitions[src] = [(None, 'fetch')]
                else:
                    for action, result in actions.items():
                        dst = (result["name"], result["state"])
                        if dst in self.transitions:
                            self.transitions[dst].append((src, action))
                        else:
                            self.transitions[dst] = [(src, action)]

    def set_order(self, orders):
        self.orders = orders
            
    def go_to(self, target_tile: Tile.Tile):
        if target_tile is None:
            print("Erreur : tile cible est None")
            self.state = "IDLE"
            self.path = None
            self.target = None
            return

        self.target = target_tile  # <-- essentiel pour l'interaction
        self.path = self.get_path(target_tile)
        if self.path is None:
            print(f"Erreur : chemin vers {target_tile.tile_type} non trouvé")
            self.state = "IDLE"
        else:
            self.state = "WALKING"


    def get_path(self, target_tile):
        start_node = Node(None, (self.x, self.y))
        end_node = Node(None, (target_tile.col, target_tile.row))
        open_list = [start_node]
        closed_set = set()
        movements = [(0,-1),(0,1),(-1,0),(1,0)]

        while open_list:
            current = heapq.heappop(open_list)
            closed_set.add(current.position)

            if abs(current.position[0] - target_tile.col) + abs(current.position[1] - target_tile.row) == 1:
                path = []
                c = current
                while c:
                    path.append(c.position)
                    c = c.parent
                return path[::-1][1:]

            for move in movements:
                nx, ny = current.position[0]+move[0], current.position[1]+move[1]
                if not (0 <= nx < self.maps.width and 0 <= ny < self.maps.height): 
                    continue
                if (nx, ny) in closed_set: 
                    continue
                tile = self.maps.grid[ny][nx]
                if tile.tile_type != "floor":
                    continue
                new_node = Node(current, (nx, ny))
                new_node.g = current.g + 1
                new_node.h = abs(nx - end_node.position[0]) + abs(ny - end_node.position[1])
                new_node.f = new_node.g + new_node.h

                for n in open_list:
                    if new_node == n and new_node.g >= n.g:
                        break
                else:
                    heapq.heappush(open_list, new_node)

        return None



    def see(self):
        if not self.orders:
            return None

        plans = []
        visited = set()

        def dfs(current, path):
            if current in visited:
                return
            visited.add(current)
            if current not in self.transitions:
                plans.append(path[::-1])
                return
            for src, action in self.transitions[current]:
                dfs(src, path + [(action, current)])

        for ingredient in self.orders[0].desired_dish.ingredients:
            dfs(ingredient.as_tuple(), [])

        self.plans = plans

    def next(self, chained_list: list):
        for recipe in chained_list[0]:
            for assemble in recipe:
                if self.itemHeld is not None and self.itemHeld.name == assemble.t2.name:
                    self.go_to("")
                    self.state = "WALKING"
                    continue

                if assemble[0] == Cook:
                    self.state = "COOKING"
                elif assemble[0] == Fry:
                    self.state = "FRYING"
                elif assemble[0] == Chop:
                    self.state = "CHOPPING"

    def action(self):
        match getattr(self, "state", "IDLE"):
            case "WALKING":
                if not self.path:
                    if isinstance(self.target, Station):
                        self.state = "INTERACT"
                    else:
                        self.state = "IDLE"
                        if self.targets:
                            self.targets.pop(0)
                    return
                self.x, self.y = self.path[0]
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                self.path = self.path[1:]

            case "INTERACT":
                if isinstance(self.target, Station):
                    if isinstance(self.target, Fridge):
                        self.interact(self.target, ingredient )
                    self.interact(self.target)
                    self.state = "IDLE"
                    if self.targets:
                        self.targets.pop(0)
                    self.target = None

            case "IDLE":
                pass


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.itemHeld is not None:
            item_rect = self.itemHeld.image.get_rect(center=self.rect.center)
            surface.blit(self.itemHeld.image, item_rect.topleft)

    def grab(self, item : Item):
        if self.itemHeld is None:
            self.itemHeld = item
            print(f"{self} picked up {item}.")
        else:
            print(f"{self} cannot pick up item; hands are full.")

    def interact(self, station : Station):
        station.interact(self)

    def interact(self, fridge : Fridge, ingredient: Ingredient):
        fridge.interact(self, ingredient)
            