from Ingredient import Ingredient

# Ingrédients
fries = Ingredient("Fries")
cooked_potato = Ingredient("Cooked Potato")
chopped_potato = Ingredient("Chopped Potato")
potato = Ingredient("Potato")

chopped_tomato = Ingredient("Chopped Tomato")
tomato = Ingredient("Tomato")

chopped_lettuce = Ingredient("Chopped Lettuce")
lettuce = Ingredient("Lettuce")

steak_cooked = Ingredient("Cooked Steak")
steak_raw = Ingredient("Steak")

# Liaisons fixes (prédefinies)
potato.evolutions = {"chop": chopped_potato, "cook": cooked_potato}
chopped_potato.evolutions = {"fry": fries}

tomato.evolutions = {"chop": chopped_tomato}
lettuce.evolutions = {"chop": chopped_lettuce}

steak_raw.evolutions = {"cook": steak_cooked}

# Création des liens précédents
for parent in [potato, chopped_potato, tomato, lettuce, steak_raw]:
    for action, child in parent.evolutions.items():
        child.previous = (parent, action)
