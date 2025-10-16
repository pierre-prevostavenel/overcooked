### player.py :
import pygame
import random

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
                    pass
                case "FRYING":
                    pass
                case "CHOPPING":
                    pass

        if len(self.orders)>0 :
            # print(self.orders[0])
            # print(self.orders[0].desired_dish)
            
            # print(self.see(self.orders[0].desired_dish.ingredients))
            pass

    def see(self, action):      
        if(action.get_super_name() == "Ingredient"):
            return [action]
        else:
            if action.__class__.__name__ == "Assemble":
                
                naction1 = action.target[0]
                # print(naction1)
                naction2 = action.target[1]
                return [self.see(naction1), self.see(naction2)]
            else :
                naction = action.target
                return [action] + self.see(naction)

    def rmv_order(self,o):
        self.orders.remove(o)
    
    def add_order(self,o):
        self.orders.append(o)

    def go_to(self, target: str, level_index):
        self.path = self.maps.get_path(self.x, self.y, target, level_index)
        if self.path is None:
            print("Erreur : chemin non trouvé")
        else:
            self.state = "WALKING"
            self.path = self.maps.get_path(self.x, self.y, target, level_index)

    def interact(self, target: str, time: int):
        """Interagit avec la target pendant un nombre de ticks défini"""
        pass

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft) 

    def next(self, chained_list: list): # exemple [[Salade->ChoppedSalad,Meat->CookedMeat],[Salade->ChoppedSalad,Meat->CookedMeat]]
        for chained_recipe in chained_list[0]:
            for chained_action in chained_recipe:

                # Regarder si chained_action[1] est déjà réalisée

                if chained_action[0] == Cook:
                    self.state = "COOKING" # arriver à transmettre l'élément à traiter

                if chained_action[0] == Fry:
                    self.state = "FRYING"

                if chained_action[0] == Chop:
                    self.state = "CHOPPING"
        