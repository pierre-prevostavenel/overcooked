### player.py :
import pygame
from Ingredient import IngredientGraph

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        self.maps = maps
        self.x =x
        self.y = y
        self.orders = []
        self.position = y * self.map_width + x
        self.manual_control = False

        self.move_cooldown = 0
        self.move_timer = 20
        self.interaction_progress = 0

        self.itemHeld = None

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
        # Toutes les 1/2s (30 ticks)
        self.move_timer += 1
        self.move_timer %=30
        if self.move_timer == 0:
            print("i see :",self.see())
            self.action()

    def set_order(self, o):
        self.orders = o
    
    def go_to(self, target: str, level_index):
        self.path = self.maps.get_path(self.x, self.y, target, level_index)
        if self.path is None:
            print("Erreur : chemin non trouvé")
            self.state = "IDLE"
        else:
            self.state = "WALKING"
            self.path = self.maps.get_path(self.x, self.y, target, level_index)

    #TODO REWORK
    def see(self):      
        """Retourne un plan d'action pour atteindre le goal (name, state)"""
        if len(self.orders) == 0:
            return None
        
        plans = []
        visited = set()
        def dfs(current, path):
            if current in visited:
                return
            visited.add(current)
            if not current in IngredientGraph.transitions:
                plans.append(path[::-1])
                return
            for src, action in IngredientGraph.transitions[current]:
                dfs(src, path + [(action, current)])
        print("I want : ", self.orders[0].desired_dish.ingredients[0].as_tuple())
        dfs(self.orders[0].desired_dish.ingredients[0].as_tuple(), [])
        return plans 



    def next(self, chained_list: list): # exemple [[Salade->ChoppedSalad,Meat->CookedMeat],[Salade->ChoppedSalad,Meat->CookedMeat]]
        for recipe in chained_list[0]:  # exemple [Salade->ChoppedSalad,Meat->CookedMeat] 
            for assemble in recipe: # exemple Salade->ChoppedSalad (objet de type Assemble)

                # Regarder si assemble.t2 est déjà réalisée
                if self.itemHeld is not None and self.itemHeld.name == assemble.t2.name:
                    # Amener l'aliment à l'assiette
                    self.go_to("")
                    self.state = "WALKING" # to plate # puis déposer l'élément dans l'asssiette
                    continue
                
                # Regarder si le player est à la bonne table (position) pour l'aliment
                
                if assemble[0] == Cook:
                    self.state = "COOKING" # arriver à transmettre l'élément à traiter

                if assemble[0] == Fry:
                    self.state = "FRYING"

                if assemble[0] == Chop:
                    self.state = "CHOPPING"
    
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
                    self.state = "IDLE" # il faut faire des self.next je pense, ça représente bien le schéma
            case "CHOPPING":
                if self.interact("workbench") == 0:
                    self.state = "IDLE"
            case "PLATING":
                if self.interact("plate") == 0:
                    self.state = "IDLE"
                    #self.orders[0].remove(done_ingredient)
            case "COLLECT":
                if self.interact("food_generatir") == 0:
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