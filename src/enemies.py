from Enemy import Enemy
from Animation import Animation
from graphics import GR
import random

defaultanimspeed = 1000

raisewing = Animation(["flyingchimney7", "flyingchimney4"], 100, False)
lowerwing = Animation(["flyingchimney5", "flyingchimney6"], 60, False)
chimneyanimation = Animation([raisewing, lowerwing], 600)
chimneyanimation.updatealwaysbattle = True

stevewave = [Animation(["scarysteven05", "scarysteven06"], 1/2),
             Animation(["scarysteven07", "scarysteven08"], 1/2),
             Animation(["scarysteven09", "scarysteven10"], 1/2),
             Animation(["scarysteven11", "scarysteven12"], 1/2),
             Animation(["scarysteven13", "scarysteven14"], 1/2),
             Animation(["scarysteven15", "scarysteven16"], 1/2)]

for a in stevewave:
    a.relativeframerate = True

stevehat = [Animation(["scarysteven17", "scarysteven18", "scarysteven19", "scarysteven20"], 1/4),
            Animation(["scarysteven21", "scarysteven22", "scarysteven23", "scarysteven24"], 1/4),
            Animation(["scarysteven25", "scarysteven26", "scarysteven27", "scarysteven28"], 1/4),
            Animation(["scarysteven29", "scarysteven30", "scarysteven31", "scarysteven32"], 1/4),
            Animation(["scarysteven33", "scarysteven34", "scarysteven35"], 1/4)]

for a in stevehat:
    a.relativeframerate = True
    a.loopp = False

steveanimation = Animation(["scarysteven00", "scarysteven01", "scarysteven02", "scarysteven03", "scarysteven04"]+stevewave+stevehat, defaultanimspeed)
steveanimation.updatealwaysbattle = True
            
animations = [Animation(["sheep0", "sheep1", "sheep2", "sheep3"], defaultanimspeed/2),
              Animation(["meangreen0", "meangreen1"], defaultanimspeed),
              Animation(["purpleperp0", "purpleperp1", "purpleperp2", "purpleperp3"], defaultanimspeed),
              Animation(["spoe0", "spoe1"], defaultanimspeed),
              Animation(["croc0", "croc1"], defaultanimspeed),
              Animation(["kewlcorn0", "kewlcorn1", "kewlcorn2", "kewlcorn3"], defaultanimspeed),
              Animation(["bugo0","bugo1"], defaultanimspeed),
              chimneyanimation,
              steveanimation,
              Animation(["radturtle0", "radturtle1"], defaultanimspeed),
              Animation(["dancelion0", "dancelion1"], defaultanimspeed)]

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
spoe = Enemy(counter, 1, "spoe", ["rests", "skippy", "melodic", "repeatvariation"])
counter += 1
croc = Enemy(counter, 1, "croc", ["melodic", "repeatmove"])
counter += 1
kewlcorn = Enemy(counter, 1, "kewlcorn", ["repeatvalues", "highrepeatchance"])
counter += 1
bugo = Enemy(counter, 1, "bogo", ["repeatvariation", "repeatmove", "highrepeatchance"])
counter += 1
chimney = Enemy(counter, 1, "chimney", ["repeatrhythm", "melodic", "highrepeatchance"])
counter += 1
steve = Enemy(counter, 1, "scary steven", ["norests", "nochords", "shorternotes", "melodic", "repeatspaceinbetween", "repeatonlybeginning", "nodoublerepeats"])
counter += 1
radturtle = Enemy(counter, 1, "rad turtle", ["repeatmove", "repeatspaceinbetween", "nodoublerepeats"])
counter += 1
dancelion = Enemy(counter, 1, "dance lion", ["alternating", "repeatvariation", "repeatonlybeginning", "nodoublerepeats"])

woodsenemies = [perp, spoe, croc, bugo, radturtle]

def random_enemy(area):
    if area == "woods":
        return random.choice(woodsenemies)
    else:
        return random.choice(woodsenemies)
