class Client(MySprite):
    def __init__(self, rect, image_path=None, fallback_color=(255, 0, 0), layer=0, patience_meter=3600):
        super().__init__()
        self.patience_meter = patience_meter
        self.desired_dish = Dish.random_dish()
        self.state = "COMMANDING"

    def accept(self, dish):
        return self.desired_dish == dish 

    def __str__():
        return super.__str__() + f"desired dish={desired_dish}"

    def update():
        match state:
            case "COMMANDING" :
                self.walk()
                
            case "WALKING_TO_EMPTY_TABLE": 
                table_coord = get_nearest_empty_table(self.posX, self.posY)
                self.walk(table_coord)

            case "WAITING":
                self.patience_meter -= 1
                if (self.patience_meter <= 0):
                    self.state="GETTING_OUT"
                    game.update_order(self,False)

            case "GETTING_OUT":
                self.walk(game.get_nearest_way_out())
        self.draw()
            
    def walk():

    def draw()