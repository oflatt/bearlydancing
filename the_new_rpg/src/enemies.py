from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

# refer to randombeatmap for the definitions for beatmap rules
sheep = Enemy(Animation([GR["sheep0"], GR["sheep1"]], 1), 0.5, "sheep", [])
greenie = Enemy(Animation([GR["meangreen0"], GR["meangreen1"]], 1), 0.3, "mean greenie",
                ["melodic", "skippy", "repeat", "cheapending"])
perp = Enemy(Animation([GR["purpleperp0"], GR["purpleperp1"], GR["purpleperp2"], GR["purpleperp3"]], 1),
             0.2, "perp", ["alternating"])

def random_enemy():
    possibles = globals()
    return possibles[random.choice(list(possibles.keys()))]