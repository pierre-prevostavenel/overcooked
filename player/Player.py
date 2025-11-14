import heapq
import pygame
import json
import food.Ingredient as Ingredient
import maps.Item as Item
import math
from food.Dish import Plate

from maps.Station import Fridge, Station, Workbench

class Player(pygame.sprite.Sprite):
    def __init__(self, json_path, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        self.x = x
        self.y = y
        
        self.position = y * self.map_width + x
        self.manual_control = False
        # pré-calcul de plans pour réaliser les recettes
        self.transitions = {}
        self.init_transitions(json_path)

        self.move_cooldown = 0
        self.move_timer = 20
        self.interaction_progress = 0

        self.state = "IDLE"
        self.itemHeld = None
        self.plans = None
        self.current_recipe = None
        self.itemWanted = None
        self.path = []

        try:
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        except pygame.error:
            print("Attention : L'image 'assets/player.png' n'a pas été trouvée.")
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size, y * tile_size)
        

    def update(self, E):
        # Toutes les 1/4s (30 ticks)
        self.move_timer += 1
        self.move_timer %=15
        if self.move_timer == 0:
            self.next(self.see(E))
            self.action()

    def see(self, E): 
        """Perçoit l'environnement et retourne les informations nécessaires à la décision."""
        per = {
            "orders": E.get_orders(),
            "game": E,
            "map": E.get_maps()
        }
        return per

    def next(self, per):
        if  (self.state != "WALKING") and (self.state != "IDLE"):
            return 
        
        orders = per["orders"]
        game = per["game"]
        map = per["map"]
        print("ORDERS RECEIVED IN NEXT: ", orders)
        if not orders:
            return
        print("CURRENT PLANS AVANT: ", self.plans)
        print("CURRENT AVANT :", self.current_recipe)

        # Si aucune recette en cours, on en génère une
        if self.plans is None:
            self.plans = self.create_plan(orders)
            print("Nouvelle recette :", self.current_recipe)
            self.pending_plate = Plate(orders[0].desired_dish.name)
            return

        #Si la recette est vide (on a fait toutes les actions qu'on devait faire) : on envoie l'asiette
        if not self.plans:
            if self.go_to(map, "table"):
                print("Recette finie !")
                self.state = "SENDING"
                self.target_game = game 
            return

        #Si on a fini la sous-recette on fait la suivante
        if self.current_recipe is None :
            # print("Changement de sous recette")
            self.current_recipe = self.plans[0]
            return

        # Si sous-recette terminée : ajout à l'assiette
        if not self.current_recipe:
            if self.go_to(map, "table"):
                # print("Ingrédient terminé, préparation du dressage")
                self.state = "PLATING"
            return
            
        # Sinon on suit le plan
        task = self.current_recipe[0]
        action, (item_name, _) = task
        self.itemWanted = item_name
        self.pending_action = action

        destinations = {
            "fetch": "fridge",
            "cook": "oven",
            "chop": "workbench"
        }

        target = destinations.get(action)
        if not target:
            print("Action inconnue :", action)
            self.state = "IDLE"
            return
        
        if self.go_to(map, target):
            print("Prêt à interagir avec", target)
            match self.pending_action:
                case "fetch":
                    self.state = "COLLECT"
                case "cook" | "fry":
                    self.state = "COOKING"
                case "chop":
                    self.state = "CHOPPING"
                case _:
                    print("Action inconnue :", self.pending_action)
                    self.state = "IDLE"

    #TODO : à adapter
    def action(self):
        """Exécute concrètement l’action décidée selon l’état."""
        # print(f"État : {self.state}, Objet tenu : {self.itemHeld}")
        # print("CURRENT PLANS APRES: ", self.plans)
        # print("CURRENT APRES :", self.current_recipe)
        
        match self.state:
            case "WALKING":
                try:
                    self.x, self.y = self.path[0]
                    self.position = self.x * self.map_width + self.y
                    self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                except TypeError:
                    print("Erreur : self.path =", self.path)

            case "COLLECT"|"COOKING"|"CHOPPING":
                if self.interact(self.target_station) == 0:
                    self.current_recipe.pop(0)
                    self.state = "IDLE"

            case "PLATING":
                if self.interact("plate") == 0:
                    # Utilise la plate préparée dans next()
                    self.pending_plate.add_ingr(self.itemHeld)
                    # print("Plate après ajout : ", self.pending_plate)

                    self.plans.pop(0)
                    self.itemHeld = None
                    self.current_recipe = None
                    print("Ingredient déposé dans l'assiette")
                    self.state = "IDLE"

            case "SENDING":
                if self.interact("plate") == 0:
                    print("Plate envoyée : ", self.pending_plate)
                    self.target_game.accept_plate(self.pending_plate)
                    
                    self.itemHeld = None
                    self.current_recipe = None
                    self.pending_plate = None
                    self.plans = None
                    print("Assiette envoyée en salle !")
                    self.state = "IDLE"

            case "IDLE":
                pass


    def init_transitions(self,json_path):
        with open(json_path, "r") as f:
            data = json.load(f)

        for ing_data in data.get("ingredients", []):
            name = ing_data["name"]
            for state_data in ing_data.get("states", []):
                state = state_data["state"]
                src = (name, state)
                actions = state_data.get("actions", {})
                if state == "raw":
                    self.transitions[src] = [(None,"fetch")]
                for action, result in actions.items():
                    dst = (result["name"], result["state"])

                    if dst in self.transitions:
                        self.transitions[dst].append((src, action))
                    else:
                        self.transitions[dst] = [(src, action)]
    
    def create_plan(self, orders):
        if len(orders) == 0:
            return None

        plans = []
        for ingredient in orders[0].desired_dish.ingredients:
            path = []
            current = ingredient.as_tuple()
            while current in self.transitions:
                src, action = self.transitions[current][0]  
                path.append((action, current)) 
                current = src  
            plans.append(path[::-1])  
        # print("COMMANDE : ", orders[0].desired_dish.ingredients)
        # print("PLANS : ", plans)
        return plans
    
    def go_to(self, map, target: str):
        """Prepare le bot à se déplacer vers target, renvoi si il est arrivé à destination ou non"""
        self.target_station = self.get_nearest(map, target)
        if self.target_station is None:
            print(f"Erreur : {target} introuvable sur la map")
            self.state = "IDLE"
            return False
        
        self.path = self.get_path(map, self.target_station)
        if self.path is None:
            print(f"Erreur : chemin vers {target.tile_type} non trouvé")
            self.state = "IDLE"
        else:
            self.state = "WALKING"
        return len(self.path) == 0   
    
    def get_nearest(self, map, tile_type):
        nearest = None
        min_dist = float('inf')
        for r in range(map.height):
            for c in range(map.width):
                tile = map.grid[r][c]
                if tile.tile_type == tile_type:
                    dist = math.hypot(c - self.x, r - self.y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = tile
        return nearest

    def get_path(self, map, target_tile):
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
                if not (0 <= nx < map.width and 0 <= ny < map.height): 
                    continue
                if (nx, ny) in closed_set: 
                    continue
                tile = map.grid[ny][nx]
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

    def grab(self, item : Item):
        if self.itemHeld is None:
            self.itemHeld = item
            print(f"{self} picked up {item}.")
        else:
            print(f"{self} cannot pick up item; hands are full.")
        
    def interact(self, station: Station):
        """
        Laisse le Fridge créer l'Ingredient au moment de l'interaction.
        ingredient_name et state sont juste des paramètres pour l'état initial.
        """
        #TODO : faire une station Table pour gérer le plating et l'envoi en salle
        if(station == "plate"):
            if self.itemHeld is None:
                print(f"{self} has nothing to interact with the plate.")
                return 0
            else:
                print(f"{self} is interacting with the plate holding {self.itemHeld}.")
                return 0  # Interaction instantanée pour le plating/sending
            
        return station.interact(self)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.itemHeld is not None:
            item_rect = self.itemHeld.image.get_rect(center=self.rect.center)
            surface.blit(self.itemHeld.image, item_rect.topleft)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f