import random, copy
from typing import List, Union


import variables, devoptions
from variables import devprint
from Enemy import Enemy
from Animation import Animation
from MultiPartAnimation import AnimationPart, MultiPartAnimation
from graphics import getpic

defaultanimspeed = 1000

# build the octopus
octopus_parts = []
# load the head
octopus_head = []
for i in range(variables.numberofoctopusheads):
    octopus_head.append(AnimationPart("octopus/head" + str(i)))
octopus_parts.append(octopus_head)
octopus_arms = []


for i in variables.octopusarmdraworder:
    armupdown = []
    
    armupdown.append(AnimationPart("octopus/arm" + str(i) + "-0"))
    armupdown.append(AnimationPart("octopus/arm" + str(i) + "-1"))

    octopus_arms.append(armupdown)
    
octopus_parts.extend(octopus_arms)

# add the body of the octopus
octopus_parts.append([AnimationPart("octopus/body")])

# now flip the list, because the body and the arms are drawn before the head
octopus_parts.reverse()

octopus_width = 20 # dummy values for novideomode
octopus_height = 20
if not devoptions.args.novideomode:
    octopus_width = getpic("octopus/body").get_width()
    octopus_height = getpic("octopus/body").get_height()

octopus_animation = MultiPartAnimation(octopus_parts,
                                       octopus_width,
                                       octopus_height)


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

stevelist : List[Union[Animation, str]] = ["scarysteven00", "scarysteven01", "scarysteven02", "scarysteven03", "scarysteven04"]+stevewave+stevehat # type: ignore
    
steveanimation = Animation(stevelist, defaultanimspeed)
steveanimation.updatealwaysbattle = True
            
animations = []

enemies = {}

counter = 0


def addEnemy(name, rules, animation, volumeenvelope=None, drumpackname=None, defaultnotes=None):
    global counter
    animations.append(animation)
    enemies[name] = Enemy(counter, 1, name, rules, volumeenvelope=volumeenvelope,
                          drumpackname=drumpackname, defaultnotes=defaultnotes)
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
addEnemy("mean green", ["melodic", "repeat", "rests", "noaccidentals"],
         Animation(["meangreen0", "meangreen1"], defaultanimspeed),
         drumpackname="deepnoise",
         defaultnotes=[2, 5, 4, 2, 5, 4, 2, 5, 4, 6, 7])

addEnemy("perp", ["alternating"],
         Animation(["purpleperp0", "purpleperp1", "purpleperp2", "purpleperp3"], defaultanimspeed),
         drumpackname="chirp")

addEnemy("spoe", ["rests", "skippy", "melodic", "repeatvariation"],
         Animation(["spoe0", "spoe1"], defaultanimspeed))

addEnemy("croc", ["melodic", "repeatmove"],
         Animation(["croc0", "croc1"], defaultanimspeed))

addEnemy("kewlcorn", ["repeatvalues", "highrepeatchance"],
         Animation(["kewlcorn0", "kewlcorn1", "kewlcorn2", "kewlcorn3"], defaultanimspeed))

addEnemy("bogo", ["repeatvariation", "repeatmove", "highrepeatchance", "highervalues"],
         Animation(["bugo0","bugo1"], defaultanimspeed))

addEnemy("chimney", ["repeatrhythm", "melodic", "highrepeatchance"],
         chimneyanimation)

addEnemy("scary steven", ["norests", "nochords", "shorternotes", "melodic", "repeatspaceinbetween", "repeatonlybeginning", "nodoublerepeats", "lowervalues"],
         steveanimation, "flat",
         drumpackname = "oomphwave")

addEnemy("rad turtle", ["repeatmove", "repeatspaceinbetween", "nodoublerepeats"],
         Animation(["radturtle0", "radturtle1"], defaultanimspeed))

addEnemy("dance lion", ["alternating", "repeatvariation", "repeatonlybeginning", "nodoublerepeats"],
          Animation(["dancelion0", "dancelion1"], defaultanimspeed))

addEnemy("pile o' snow", ["melodic", "repeat", "repeatvariation", "seperatedchordchance"],
         Animation(["pileo'snow0", "pileo'snow1"], defaultanimspeed))

# TODO change to hopping tree
addEnemy("hopping tree", ["melodic", "holdlongnote"],
         Animation(["chicking0"],defaultanimspeed))

addEnemy("snow fly", ["melodic", "repeatvariation", "doublenotes"],
         Animation(["snowbutterflyfly0", "snowbutterflyfly1"], defaultanimspeed))

addEnemy("polar giraffe", ["melodic", "combinemelodies"],
         Animation(["polargiraffe0", "polargiraffe1"], defaultanimspeed))

addEnemy("yoyo", ["drummer"], octopus_animation)

woodsenemies = getenemies(["perp", "spoe", "croc", "bogo", "rad turtle"])
snowenemies = getenemies(["pile o' snow", "snow fly", "polar giraffe"])

# if none picks random one, if an enemy engages enemy
devbattletest = enemies["bogo"]

def random_enemy(area):
    return random.choice(woodsenemies)

def enemyforspecialbattle(enemyname):
    return copy.copy(enemies[enemyname])
