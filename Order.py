from Dish import Dish

class Order:
    def __init__(self, total_time=60):
        self.desired_dish = Dish.random_dish()
        self.time_remaining = total_time * 60

    def accept_order(self, dish):
        return Dish.equal(self.desired_dish, dish)
    
    #update le temps restant d'une commande, renvoie si la commande est encore active ou non.
    def update(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            return True
        return False    
    
    def __str__(self):
        return "je commande : " + self.desired_dish.__str__()
