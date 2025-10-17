### player.py :
import pygame
import json
from Ingredient import Ingredient

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, food_json_path, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        self.maps = maps
        self.x =x
        self.y = y
        
        self.position = y * self.map_width + x
        self.manual_control = False

        # pré calcul de plans pour réaliser les recettes
        self.transitions = {}
        self.init_transitions(food_json_path)

        self.move_cooldown = 0
        self.move_timer = 20
        self.interaction_progress = 0

        self.itemHeld = None
        self.current_recipe = None
        self.itemWanted = None
        self.plans = []

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
        # Toutes les 1/2s (30 ticks)
        self.move_timer += 1
        self.move_timer %=30
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
    
    def go_to(self, target: str, level_index):
        self.path = self.maps.get_path(self.x, self.y, target, level_index)
        if self.path is None:
            print("Erreur : chemin non trouvé")
            self.state = "IDLE"
        else:
            self.state = "WALKING"
            self.path = self.maps.get_path(self.x, self.y, target, level_index)

    #TODO REWORK
    def see(self, E):      
        per = E.get_orders()
        return per

    def next(self, per): 
        
        """Retourne un plan d'action pour atteindre le goal (name, state)"""
        if len(self.orders) == 0:
            return None
        
        if self.current_recipe is None:
            plans = []
            visited = set()
            def dfs(current, path):
                if current in visited:
                    return
                visited.add(current)
                if not current in self.transitions:
                    plans.append(path[::-1])
                    return
                for src, action in self.transitions[current]:
                    dfs(src, path + [(action, current)])
            print("I want : ", per[0].desired_dish.ingredients[0].as_tuple())
            print(per[0].desired_dish.ingredients)
            for i in (per[0].desired_dish.ingredients): 
                print(i)
                dfs(i.as_tuple(), [])
            self.plans = plans
            self.current_recipe = plans[0]

        task = self.current_recipe[0]
        for task in self.current_recipe:  # exemple ('fetch', ('steak', 'raw')) 
            destinations = {"fetch": "fridge", "cook": "gas_station", "fry": "gas_station", "chop": "workbench"}
            # A côté de la case recherchée
            if len(self.maps.get_path(self.x, self.y, destinations[task[0]], level_index)) == 2:
                # On est à côté d'une case de type destinations[recipe[0]]
                if destinations[task[0]] == "fridge":
                    self.itemWanted = task[1][0]
                    self.state = "COLLECT"
                else:  # On n'est pas sur un frigo, donc on fait une interaction
                    self.itemWanted = task[1][0]
                    self.interact(destinations[task[0]])
                # On supprime la tâche de ce qu'il fallait faire
                self.current_recipe = [1:]
            else:  # On doit se rendre à la case
                match recipe[0]:
                # NON if chemin du go_to a une longueur de 2 : on est à côté de la case
                
                    case "fetch":
                        self.go_to("fridge")
                    case "cook":
                        self.go_to("gas_station")
                    case "fry":
                        self.go_to("gas_station")
                    case "chop":
                        self.go_to("workbench")
                    case _:
                        print("On ne sait pas quoi faire")
        
    def action(self):
        match self.state:
            case "WALKING":
                try:
                    self.x, self.y = self.path[0]
                    self.position = self.x*self.map_width+self.y
                    self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                    if len(self.path) == 2:  # On s'arrête quand on est à côté de la case visée
                        self.path = []
                        self.state = "IDLE"
                    else:
                        self.path = self.path[1:]
                except TypeError:
                    print(f"self.path: {self.path}")
            case "IDLE":
                print("idle player")
            case "COOKING":
                if self.interact("gas_station") == 0:  # Nombre de ticks restants sur la tâche
                    self.itemHeld.apply_action("cook")
                    self.state = "IDLE" 

            case "CHOPPING":
                if self.interact("workbench") == 0:
                    self.itemHeld.apply_action("chop")
                    self.state = "IDLE"
            case "PLATING":
                if self.interact("plate") == 0:
                    self.state = "IDLE"
                    # Ajouter à l'assiette l'élément dans la main
                    self.itemHeld = None  # On vide la main
                    # self.orders[0].remove(done_ingredient)
            case "COLLECT":
                if self.interact("fridge") == 0:
                    self.itemHeld = Ingredient(self.itemWanted)  # On ajoute à l'inventaire un élément
                    self.state = "IDLE"

                    
    def interact(self, target: str):
        """Interagit avec la target pendant un nombre de ticks défini"""
        if self.interaction_progress == 0:  # On appelle une interaction mais on ne fait rien actuellement : on détermine la durée de l'interaction
            match target:
                case "gas_station":
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