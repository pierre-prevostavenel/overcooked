from Ingredient import Ingredient  

fries = Ingredient("Fries")
cooked_potato = Ingredient("Cooked Potato")
chopped_potato = Ingredient("Chopped Potato", next_stages=[fries])
potato = Ingredient("Potato", next_stages=[chopped_potato, cooked_potato])

chopped_tomato = Ingredient("Chopped Tomato")
tomato = Ingredient("Tomato", next_stages=[chopped_tomato])

chopped_lettuce = Ingredient("Chopped Lettuce")
lettuce = Ingredient("Lettuce", next_stages=[chopped_lettuce])

steak_cooked = Ingredient("Cooked Steak")
steak_raw = Ingredient("Steak", next_stages=[steak_cooked])