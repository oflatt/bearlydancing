from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

animations = [Animation([GR["sheep0"], GR["sheep1"]], 1),
              Animation([GR["meangreen0"], GR["meangreen1"]], 1),
              Animation([GR["purpleperp0"], GR["purpleperp1"], GR["purpleperp2"], GR["purpleperp3"]], 1)]

# refer to randombeatmap for the definitions for beatmap rules
#we use a animation number because the actual animation cannot be saved
counter = 0
sheep = Enemy(counter, 0.5, "sheep", ["cheapending"])
counter += 1
greenie = Enemy(counter, 0.3, "mean greenie",
                ["melodic", "skippy", "cheapending", "repeat"])
counter += 1
perp = Enemy(counter,
             0.2, "perp", ["alternating", "cheapending"])

def random_enemy():
    possibles = globals()
    return possibles[random.choice(list(possibles.keys()))]