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
            
animations = []

enemies = {}

counter = 0
def addEnemy(name, rules, animation):
    global counter
    animations.append(animation)
    enemies[name] = Enemy(counter, 1, name, rules)
    counter += 1

def getenemies(listofnames):
    l = []
    for n in listofnames:
        l.append(enemies[n])
    return l

# refer to randombeatmap for the definitions for beatmap rules
# we use an animation number because the actual animation cannot be saved

# sheep is a simple random one
addEnemy("sheep", [],
         Animation(["sheep0", "sheep1", "sheep2", "sheep3"], defaultanimspeed/2))

# just tutorial enemy
addEnemy("mean green", ["melodic", "repeat", "rests"],
         Animation(["meangreen0", "meangreen1"], defaultanimspeed))

addEnemy("perp", ["alternating"],
         Animation(["purpleperp0", "purpleperp1", "purpleperp2", "purpleperp3"], defaultanimspeed))

addEnemy("spoe", ["rests", "skippy", "melodic", "repeatvariation"],
         Animation(["spoe0", "spoe1"], defaultanimspeed))

addEnemy("croc", ["melodic", "repeatmove"],
         Animation(["croc0", "croc1"], defaultanimspeed))

addEnemy("kewlcorn", ["repeatvalues", "highrepeatchance"],
         Animation(["kewlcorn0", "kewlcorn1", "kewlcorn2", "kewlcorn3"], defaultanimspeed))

addEnemy("bogo", ["repeatvariation", "repeatmove", "highrepeatchance"],
         Animation(["bugo0","bugo1"], defaultanimspeed))

addEnemy("chimney", ["repeatrhythm", "melodic", "highrepeatchance"],
         chimneyanimation)

addEnemy("scary steven", ["norests", "nochords", "shorternotes", "melodic", "repeatspaceinbetween", "repeatonlybeginning", "nodoublerepeats"],
         steveanimation)

addEnemy("rad turtle", ["repeatmove", "repeatspaceinbetween", "nodoublerepeats"],
         Animation(["radturtle0", "radturtle1"], defaultanimspeed))

addEnemy("dance lion", ["alternating", "repeatvariation", "repeatonlybeginning", "nodoublerepeats"],
          Animation(["dancelion0", "dancelion1"], defaultanimspeed))

addEnemy("pile o' snow", [],
         Animation(["pileo'snow0", "pileo'snow1"], defaultanimspeed))


woodsenemies = getenemies(["perp", "spoe", "croc", "bogo", "rad turtle"])
snowenemies = getenemies(["pile o' snow"])

# if none picks random one, if an enemy engages enemy
devbattletest = enemies["bogo"]

def random_enemy(area):
    return random.choice(woodsenemies)
