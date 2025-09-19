from MySprite import MySprite
class Client(MySprite):
    def __init__(self, posX, posY, image_path=None, fallback_color=(255, 0, 0), layer=0, patience_meter=3600):
        rect = pygame.Rect(posX, posY, 32, 32)  # ou une autre taille selon ton sprite
        super().__init__(rect, image_path, fallback_color, layer)
        self.patience_meter = patience_meter
        self.desired_dish = Dish.random_dish()
        self.state = "COMMANDING"

    def accept(self, dish):
        state="EATING"
        #game.update_order(self, True)
        return self.desired_dish == dish 

    def storm_out(self):
        self.prep_walk(game.get_nearest(self.rect.x, self.rect.y,"exit"))
        
    def prep_walk(self,target):
        self.target = target
        self.state = "WALKING"

    def update(self):
        match self.state:
            case "COMMANDING":
                #game.order(desired_dish)
                self.prep_walk(game.get_nearest(self.rect.x, self.rect.y,"table"))

            case "WALKING":
                self.walk(self.target)

            case "WAITING":
                self.patience_meter -= 1
                if self.patience_meter <= 0:
                    #game.update_order(order, False)
                    self.storm_out()

            case "EATING":
                self.patience_meter -= 1
                if self.patience_meter <= 0:
                    self.storm_out()
        self.draw()

    def walk(self, target_pos=None):
        if target_pos:
            dx = target_pos[0] - self.rect.x
            dy = target_pos[1] - self.rect.y
            step = 2  # vitesse de marche

            if abs(dx) > step:
                self.rect.x += step if dx > 0 else -step
            if abs(dy) > step:
                self.rect.y += step if dy > 0 else -step

    def draw(self):
        screen = pygame.display.get_surface()  # Ou passe le screen via un paramètre
        screen.blit(self.image, self.rect)

    def __str__():
        return super.__str__() + f"desired dish={desired_dish}"