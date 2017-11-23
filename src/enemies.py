from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

defaultanimspeed = 1000

animations = [Animation([GR["sheep0"], GR["sheep1"], GR["sheep2"], GR["sheep3"]], defaultanimspeed/2),
              Animation([GR["meangreen0"], GR["meangreen1"]], defaultanimspeed),
              Animation([GR["purpleperp0"], GR["purpleperp1"], GR["purpleperp2"], GR["purpleperp3"]], defaultanimspeed),
              Animation([GR["spoe0"], GR['spoe1']], defaultanimspeed),
              Animation([GR["croc0"], GR['croc1']], defaultanimspeed)]

# refer to randombeatmap for the definitions for beatmap rules
# we use an animation number because the actual animation cannot be saved
counter = 0
sheep = Enemy(counter, 1, "sheep", ["cheapending"])
counter += 1
greenie = Enemy(counter, 1, "mean greenie", ["melodic", "skippy", "cheapending", "repeat"])
counter += 1
perp = Enemy(counter, 1, "perp", ["alternating", "cheapending"])
counter += 1
spoe = Enemy(counter, 1, "spoe", ["rests", "melodic", "cheapending", "repeat"])
counter += 1
croc = Enemy(counter, 1, "croc", ["melodic", "cheapending", "repeatmove"])

woodsenemies = [perp, spoe, croc]

def random_enemy(area):
    if area == "woods":
        return random.choice(woodsenemies)
    else:
        return random.choice(woodsenemies)
