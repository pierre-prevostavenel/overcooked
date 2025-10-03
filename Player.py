### player.py :
import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, maps, x=1, y=2, tile_size=50):
        super().__init__()
        self.map_width = 10
        self.tile_size = tile_size
        
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
            print(self.orders[0])
            print(self.orders[0].desired_dish)
            
            print(self.see(self.orders[0].desired_dish.ingredients))

    def see(self, action):      
        if(action.get_super_name() == "Ingredient"):
            return [action]
        else:
            if action.__class__.__name__ == "Assemble":
                
                naction1 = action.target[0]
                print(naction1)
                naction2 = action.target[1]
                return [self.see(naction1), self.see(naction2)]
            else :
                naction = action.target
                return [action] + self.see(naction)


        
        self.move_cooldown = 0
        moved = False

        # Mouvement automatique aléatoire (le bloc 'if self.manual_control' a été retiré)
        mouvements_possibles = []
        if self.position >= self.map_width:
            mouvements_possibles.append(-self.map_width)
        if self.position < self.map_width * (self.map_width - 1):
            mouvements_possibles.append(self.map_width)
        if self.position % self.map_width != 0:
            mouvements_possibles.append(-1)
        if self.position % self.map_width != self.map_width - 1:
            mouvements_possibles.append(1)

        if mouvements_possibles:
            mouvement = random.choice(mouvements_possibles)
            self.position += mouvement
            moved = True
        
        if moved:
            current_col = self.position % self.map_width
            current_row = self.position // self.map_width
            self.rect.topleft = (current_col * self.tile_size, current_row * self.tile_size)
            print(f"Position du joueur : {current_col}, {current_row}")        

    def interact(self, target: str, time: int):
        """Interagit avec la target pendant un nombre de ticks défini"""
        pass

    def draw(self, surface):
        """Dessine le joueur sur la surface donnée."""
        surface.blit(self.image, self.rect.topleft) 

    def next(self, chained_list: list[list[Assemble]]): # exemple [[Salade->ChoppedSalad,Meat->CookedMeat],[Salade->ChoppedSalad,Meat->CookedMeat]]
        for chained_recipe in chained_list[0]:
            for chained_action in chained_recipe:

                # Regarder si chained_action[1] est déjà réalisée

                if chained_action[0] == Cook:
                    self.state = "COOKING" # arriver à transmettre l'élément à traiter

                if chained_action[0] == Fry:
                    self.state = "FRYING"

                if chained_action[0] == Chop:
                    self.state = "CHOPPING"
                
