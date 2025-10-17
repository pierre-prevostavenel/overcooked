### player.py :
import pygame
import json
from Ingredient import Ingredient
from Dish import *

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, food_json_path, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        self.maps = maps
        self.x = x
        self.y = y
        
        self.position = y * self.map_width + x
        self.manual_control = False

        # pré calcul de plans pour réaliser les recettes
        self.transitions = {}
        self.init_transitions(food_json_path)

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
    
    def init_transitions(self, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            for ing_name, trans_state in data["ingredients"].items():
                for state, trans in trans_state.items():
                    src = (ing_name, state)
                    for action, result in trans.items():
                        new_name = result["name"]
                        new_state = result["state"]
                        dst = (new_name, new_state)
                        if dst in self.transitions:
                            self.transitions[dst].append((src, action))
                        else:
                            self.transitions[dst] = [(src, action)]
                self.transitions[src] = [(None ,'fetch')]
    
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

    def see(self, E): 
        """Perçoit l'environnement et retourne les informations nécessaires à la décision."""
        per = {
            "orders": E.get_orders(),
            "game": E,
            # Tu peux ajouter ici d'autres perceptions plus tard (ingrédients, joueurs, etc.)
        }
        return per

    def go_to(self, target: str):
        """Prepare le bot à se déplacer vers target, renvoi si il est arrivé à destination ou non"""
        self.path = self.maps.get_path(self.x, self.y, target)
        if self.path is None:
            print("Erreur : chemin non trouvé")
            self.state = "IDLE"
        else:
            self.state = "WALKING"
            self.path = self.maps.get_path(self.x, self.y, target)
        return len(self.path) == 1

    def next(self, per):
        if  (self.state != "WALKING") and (self.state != "IDLE"):
            return 
        
        orders = per["orders"]
        game = per["game"]

        if not orders:
            return
        # print("CURRENT PLANS AVANT: ", self.plans)
        # print("CURRENT AVANT :", self.current_recipe)

        # Si aucune recette en cours, on en génère une
        if self.plans is None:
            self.plans = self.create_plan(orders)
            print("Nouvelle recette :", self.current_recipe)
            self.pending_plate = Plate(orders[0].desired_dish.name)
            return

        if not self.plans:
            if self.go_to("table"):
                print("Recette finie !")
                self.state = "SENDING"
                self.target_game = game 
            return

        if self.current_recipe is None :
            # print("Changement de sous recette")
            self.current_recipe = self.plans[0]
            return

        # Si recette terminée → préparation de l’assiette
        
        if not self.current_recipe:
            if self.go_to("table"):
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
        
        if self.go_to(target):
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

            case "COLLECT":
                if self.interact("fridge") == 0:
                    print("Collecte :", self.itemWanted)
                    self.itemHeld = Ingredient(self.itemWanted)
                    self.current_recipe.pop(0)  # étape terminée
                    self.state = "IDLE"
            case "COOKING":
                if self.interact("oven") == 0:
                    self.itemHeld.apply_action("cook")
                    self.current_recipe.pop(0)
                    self.state = "IDLE"
            case "CHOPPING":
                if self.interact("workbench") == 0:
                    self.itemHeld.apply_action("chop")
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
        
    def interact(self, target: str):
        """Interagit avec la target pendant un nombre de ticks défini"""
        if self.interaction_progress == 0:  # On appelle une interaction mais on ne fait rien actuellement : on détermine la durée de l'interaction
            match target:
                case "oven":
                    self.interaction_progress = 5
                case "workbench":
                    self.interaction_progress = 5
                case "plate":
                    self.interaction_progress = 1
                case "fridge":
                    self.interaction_progress = 1
                case _:
                    print("Erreur : interaction avec élément inconnu")
                    self.interaction_progress = 5
            return self.interaction_progress
        else:  # Une interaction est en cours, donc on la continue
            self.interaction_progress -= 1
            if self.interaction_progress < 0: self.interaction_progress = 0  # Sécurité normalement non nécessaire
            return self.interaction_progress  # On retourne le nombre de ticks restants (0 = fini)

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft) 