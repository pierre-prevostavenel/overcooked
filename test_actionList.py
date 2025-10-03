from Player import Player
from Dish import Dish
from ingredients_list import *

player = Player()
randoDish = Dish().random_dish()

print(f"Plat aléatoire généré : {randoDish}")

actions = player.get_action_list(randoDish)

for i, action_chain in enumerate(actions, start=1):
    print(f"Chaîne {i} : ", " → ".join(str(action) for action in action_chain))
