from Dish import Dish
import pygame

class Order:
    def __init__(self, t_time=60):
        self.desired_dish = Dish.random_dish()
        self.time_remaining = t_time * 60
        self.total_time = t_time * 60

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
    
    def __repr__(self):
        return self.desired_dish.__str__()

    @staticmethod
    def draw_orders(surface, orders, font, x=10, y=10):
        spacing = 40  # espace vertical réduit
        bar_width = 120
        bar_height = 6

        for i, order in enumerate(orders):
            dish = order.desired_dish
            time_ratio = order.time_remaining / order.total_time
            time_ratio = max(0, min(1, time_ratio))

            order_y = y + i * spacing

            # --- Nom du plat (police plus petite ou tronquée si besoin)
            name_text = font.render(f"{dish.name}", True, (255, 255, 255))
            surface.blit(name_text, (x, order_y))

            # --- Barre de progression plus petite
            pygame.draw.rect(surface, (50, 50, 50), (x, order_y + 18, bar_width, bar_height))  # fond
            pygame.draw.rect(surface, (0, 180, 0), (x, order_y + 18, bar_width * time_ratio, bar_height))  # remplissage

