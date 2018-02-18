from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

defaultanimspeed = 1000

animations = [Animation(["sheep0", "sheep1", "sheep2", "sheep3"], defaultanimspeed/2),
              Animation(["meangreen0", "meangreen1"], defaultanimspeed),
              Animation(["purpleperp0", "purpleperp1", "purpleperp2", "purpleperp3"], defaultanimspeed),
              Animation(["spoe0", "spoe1"], defaultanimspeed),
              Animation(["croc0", "croc1"], defaultanimspeed)]

# refer to randombeatmap for the definitions for beatmap rules
# we use an animation number because the actual animation cannot be saved
counter = 0
sheep = Enemy(counter, 1, "sheep", ["cheapending"])
counter += 1
# just tutorial enemy
greenie = Enemy(counter, 1, "mean greenie", ["melodic", "cheapending", "repeatmovevariation", "rests"])
counter += 1
perp = Enemy(counter, 1, "perp", ["alternating", "cheapending"])
counter += 1
spoe = Enemy(counter, 1, "spoe", ["rests", "skippy", "melodic", "cheapending", "repeat"])
counter += 1
croc = Enemy(counter, 1, "croc", ["melodic", "cheapending", "repeatmove"])

woodsenemies = [perp, spoe, croc]

def random_enemy(area):
    if area == "woods":
        return random.choice(woodsenemies)
    else:
        return random.choice(woodsenemies)
