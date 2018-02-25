from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

defaultanimspeed = 1000

animations = [Animation(["sheep0", "sheep1", "sheep2", "sheep3"], defaultanimspeed/2),
              Animation(["meangreen0", "meangreen1"], defaultanimspeed),
              Animation(["purpleperp0", "purpleperp1", "purpleperp2", "purpleperp3"], defaultanimspeed),
              Animation(["spoe0", "spoe1"], defaultanimspeed),
              Animation(["croc0", "croc1"], defaultanimspeed),
              Animation(["kewlcorn0", "kewlcorn1", "kewlcorn2", "kewlcorn3"], defaultanimspeed),
              Animation(["bugo0","bugo1"], defaultanimspeed)]

# refer to randombeatmap for the definitions for beatmap rules
# we use an animation number because the actual animation cannot be saved
counter = 0
# sheep is a simple random one
sheep = Enemy(counter, 1, "sheep", [])
counter += 1
# just tutorial enemy
greenie = Enemy(counter, 1, "mean greenie", ["melodic", "repeat", "rests"])
counter += 1
perp = Enemy(counter, 1, "perp", ["alternating"])
counter += 1
spoe = Enemy(counter, 1, "spoe", ["rests", "skippy", "melodic", "repeat"])
counter += 1
croc = Enemy(counter, 1, "croc", ["melodic", "repeatmove"])
counter += 1
kewlcorn = Enemy(counter, 1, "kewlcorn", ["repeatvalues", "highrepeatchance"])
counter += 1
bugo = Enemy(counter, 1, "bugo", ["repeatmovevariation", "highrepeatchance"])

woodsenemies = [perp, spoe, croc, bugo]

def random_enemy(area):
    if area == "woods":
        return random.choice(woodsenemies)
    else:
        return random.choice(woodsenemies)
