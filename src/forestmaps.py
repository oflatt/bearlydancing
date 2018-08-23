import variables, classvar, enemies, graphics, random, pygame, copy
from conversations import getconversation
from Animation import Animation
from graphics import scale_pure
from graphics import GR
from Map import Map
from Rock import Rock
from Exit import Exit
from pygame import Rect
from Conversation import Conversation
from Speak import Speak
from random import randint
from EventRequirement import EventRequirement

from mapsvars import *

# jeremyhome####################################################################################
rgrassland = graphics.grassland(800, 500)
b = GR[rgrassland]["w"]/10

hole = Rock("rabbithole", b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 1 / 2, 1, 1 / 2])

jmyman = Rock("jeremy0", b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 3 / 4, 1, 1 / 4])
jmyman.background_range = hole.background_range.copy()

dancelionanim = Animation(["dancelion0", "dancelion1"], (60000/130)*2)
dancelion = Rock(dancelionanim, b/2, b * 4, [0, 3 / 4, 1, 1 / 4])
dancelion.updatealways = True

jeremyhome = Map(rgrassland, [hole,
                              jmyman,
                              dancelion])

dontputrockslist = [dancelion.getrect(), jmyman.getrect()]
jeremyhome.populate_with("greyrock", randint(0, 2), dontputrockslist)
jeremyhome.populate_with("pinetree", randint(3, 8), dontputrockslist)
jeremyhome.populate_with("flower", randint(15, 25), dontputrockslist)

jeremyhome.exitareas = [Exit("right", False, 'outside1', "left", "same"),
                        Exit("left", False, 'tutorialwin', "right", "same")]
jeremy = getconversation("jeremy")
jeremy.area = [b * 5 + GR["rabbithole"]["w"] - (honeyw / 2), b * 5 - GR["rabbithole"]["h"],
                             GR["rabbithole"]["w"] - (honeyw / 2), GR["rabbithole"]["h"]]

dancelionpass = getconversation("dancelionpass")
dancelionpass.area = [0, 0, b, b * 10]
dancelionpass.isbutton = False
dancelionpass.exitteleport = [b + honeyw / 4, "same"]
dancelionpass.eventrequirements = [EventRequirement("beatsteve", -1, 1)]

dancelionbattle = getconversation("dancelionbattle")
dancelionbattle.eventrequirements = [EventRequirement("beatsteve")]
dancelionbattle.area = [dancelion.x, dancelion.y, dancelion.w+10, dancelion.h+10]
dancelionbattle.special_battle = copy.copy(enemies.dancelion)
dancelionbattle.special_battle.lv = 6
dancelionbattle.special_battle.specialscale = "C minor"

jeremyhome.conversations = [jeremy, dancelionpass, dancelionbattle]

# outside2######################################################################################
rgrassland = graphics.grassland(600, 500, rightpath = False, uppath = True)
outsideheight = GR[rgrassland]["h"]
b = GR[rgrassland]["w"] / 10
outside2 = Map(rgrassland, [])
outside2.populate_with("pinetree", 22)
outside2.populate_with("greyrock", 3)
outside2.populate_with("flower", randint(0, 1))

outside2.exitareas = [
    Exit("left", False, 'outside1', "right", "same"),
    Exit("top", False, 'outside3', "same", "bottom")]
outside2.enemies = enemies.woodsenemies
outside2.lvrange = [1]


# outside3######################################################################################
rgrassland = graphics.grassland(600, 500, leftpath = False, downpath = True)
b = GR[rgrassland]["w"] / 10
outsideheight = GR[rgrassland]["h"]
outside3 = Map(rgrassland, [])
outside3.populate_with("greyrock", 4)
outside3.populate_with("pinetree", 12)
outside3.populate_with("flower", randint(0, 2))
outside3.exitareas = [Exit("bottom", False, "outside2", "same", "top"),
                      Exit("right", False, "outside5", "left", "same")]
outside3.enemies = enemies.woodsenemies
outside3.lvrange = [1, 2]

# outside4/rockorsheep#########################################################################
outside4width = 800
outside4height = 600
rgrassland = graphics.grassland(outside4width, outside4height, leftpath = False, rightpath = False, uppath = True)

def make_rock_or_sheep_rocks():
    bigx = int(outside4width/2) - randint(int(outside4width/10), int(outside4width/3))
    rocklist = []
    def addgroup(number, offset, xpos):
        y = outside4height - 100 + randint(0, 20)
        x = xpos
        for i in range(number):
            sheepnum = i + offset
            rockname = "rockorsheep"
            if sheepnum < 10:
                rockname = rockname + "0" + str(sheepnum)
            else:
                rockname = rockname + str(sheepnum)
                
            rocklist.append(Rock(rockname, x, y, [0,0,1,1]))
            x += randint(30, 40)
            y += randint(-4, 4)
        return x

    bigx = addgroup(4, 0, bigx)
    bigx += 30
    bigx = addgroup(2, 4, bigx)
    bigx += 30
    addgroup(6, 6, bigx)
    return rocklist


outside4 = Map(rgrassland, [])
outside4.populate_with("greyrock", 40)
outside4.populate_with("flower", randint(3, 8))

# this is how many pixels away each dimension of the rock has to be to the sheep to work
sheeptorocktolerance = 5
def getrandomrock():
    return random.choice(outside4.terrain)

randrock = getrandomrock()

# returns true if the rock is within the sheeptorocktolerance
def sheepsizep(rrock):
    # get unscaled pure width and height to compare to the sheep picture
    rrockw = GR[rrock.animations[0].pics[0]]["img"].get_width()
    rrockh = GR[rrock.animations[0].pics[0]]["img"].get_height()
    sheepw = GR["sheepstanding"]["img"].get_width()
    sheeph = GR["sheepstanding"]["img"].get_height()
    return abs(rrockw-sheepw) <= sheeptorocktolerance and abs(rrockh-sheeph) <= sheeptorocktolerance

for x in range(3):
    if sheepsizep(randrock):
        break
    else:
        # if it does not fit try again
        randrock = getrandomrock()

randrock.animations.append(Animation(["sheepstanding"],1))
randrock.name = "sheeprock"

outside4.terrain.extend(make_rock_or_sheep_rocks())

sheepconversation = getconversation("sheepconversation")
sheepconversation.switchtheserocks = ["sheeprock"]
sheepconversation.area = [randrock.x, randrock.y, randrock.w, randrock.h]
sheepconversation.special_battle = copy.copy(enemies.sheep)
sheepconversation.special_battle.lv = 3

outside4.conversations = [sheepconversation]

outside4.exitareas = [Exit("up", False, "outside5", "same", "bottom")]
outside4.enemies = enemies.woodsenemies
outside4.lvrange = [2,3]


# outside5 #####################################################################################
outside5 = Map(graphics.grassland(800, outside4height, downpath = True), [])
outside5.populate_with("greyrock", 4)
outside5.populate_with("pinetree", 15)
outside5.populate_with("flower", randint(1, 3))
outside5.enemies = enemies.woodsenemies
outside5.lvrange = [2]
outside5.exitareas = [Exit("left", False, "outside3", "right", "same"),
                      Exit("bottom", False, "outside4", "same", "top"),
                      Exit("right", False, "outside6", "left", "same")]


# outside6 #####################################################################################
outside6width = 1200
outside6height = outside4height
groveheight = variables.TREEHEIGHT*1.5
grovewidth = variables.TREEWIDTH*3

grovetree = Rock(graphics.pinetree(),
                 outside6width/2-variables.TREEWIDTH/2,
                 outside6height-(groveheight/2)-(variables.TREEHEIGHT/2),
                 variables.TREECOLLIDESECTION)
kewlcorn = Rock("kewlcorn0", grovetree.x+variables.TREEWIDTH/2+5, grovetree.y+variables.TREEHEIGHT/4, None)
kewlcorn.name = "kewlcorn"
kewlcorn.background_range = Rect(0,kewlcorn.y+ variables.TREEHEIGHT*(3/4)-kewlcorn.h+1,9999999,9999999)
kewlcorn.hide()

outside6 = Map(graphics.grassland(outside6width, outside6height), [grovetree, kewlcorn])

# make a cleared area for the one tree
groverect = Rect(outside6width/2-grovewidth/2, outside6height-groveheight,
                 grovewidth, groveheight)

outside6.populate_with("greyrock", 6, [groverect])
outside6.populate_with("pinetree", 28, [groverect])
outside6.populate_with("flower", randint(3, 7), [groverect])

kewlappearconversation = Conversation("kewlappearconversation",[])
kewlappearconversation.area = [grovetree.x+grovetree.w/2, grovetree.y + grovetree.h*(3/4), grovetree.w/4, grovetree.h/4]
kewlappearconversation.storyevent = "kewlappears"
kewlappearconversation.eventrequirements = [EventRequirement("kewlappears", -1, 1)]
kewlappearconversation.unhidethisrock = "kewlcorn"

kewlbattle = getconversation("kewlcornyo")
kewlbattle.area = kewlappearconversation.area.copy()
kewlbattle.eventrequirements = [EventRequirement("kewlappears")]
kewlbattle.special_battle = copy.copy(enemies.kewlcorn)
kewlbattle.special_battle.lv = 4

outside6.conversations = [kewlappearconversation, kewlbattle]

outside6.enemies = enemies.woodsenemies
outside6.lvrange = [3]
outside6.exitareas = [Exit("left", False, "outside5", "right", "same"),
                      Exit("right", False, "outside7", "left", "same")]



# outside7/scary steve##########################################################################
outside7width = 1000
outside7height = outside4height

tpdance = Animation(["tpwalksright0", "tpwalksright1", "tpwalksright2", "tpwalksright3", "tpwalksright4"], 250)
tpwalking = tpdance
tp = Rock([tpdance, tpwalking], outside7width-200, outside7height/2 - 30, None, "tp")

stevedance = Animation(["scarysteven00", "scarysteven01", "scarysteven02", "scarysteven03"], (60000/130)*2)
stevewalk = stevedance
steve = Rock([stevedance, stevewalk], outside7width+1, tp.y+tp.h*2, [0,4/5,1,1/5])
steve.name = "steve"

outside7 = Map(graphics.grassland(outside7width, 600, rightpath=False), [tp, steve])
reservedarea = [Rect(tp.x-10, 0, outside7width-tp.x, outside7width)]
outside7.populate_with("greyrock", 6, reservedarea)
outside7.populate_with("pinetree", 25, reservedarea)
outside7.populate_with("flower", randint(1, 3), reservedarea)

outside7.lvrange = [3, 4]

outside7.exitareas = [Exit("left", False, "outside6", "right", "same")]

tpboss1 = getconversation("tpboss1")
tpboss1.area = [tp.x-40, 0, outside7width-(tp.x-40), outside7height]
tpboss1.storyevent = "tpboss1"
tpboss1.eventrequirements = [EventRequirement("tpboss1", -1, 1)]
tpboss1.exitteleport = [tp.x-40-honeyw-4, "same"]
tpboss1.isbutton = False

animstarter = Conversation("animstarter", [], switchtheserocks = ["tp", "steve"])
animstarter.storyevent = "tpboss1leaves"
animstarter.area = [0,0,outside7width,outside7height]
animstarter.isbutton = False
animstarter.eventrequirements = [EventRequirement("tpboss1"), EventRequirement("tpboss1leaves", -1, 1)]

scarysteve = getconversation("scarysteve")
scarysteve.area = tpboss1.area.copy()
scarysteve.area[0] += 40
scarysteve.eventrequirements = [EventRequirement("tpboss1leaves"), EventRequirement("beatsteve", -1, 1)]
scarysteve.isbutton = False
scarysteve.exitteleport = tpboss1.exitteleport.copy()
scarysteve.exitteleport[0] += 40
scarysteve.special_battle = copy.copy(enemies.steve)
scarysteve.special_battle.lv = 5
scarysteve.special_battle.storyeventsonwin = ["beatsteve"]

sagain = getconversation("steveagain")
sagain.area = [steve.x-100-3, steve.y, steve.w+6, steve.h+10]
sagainoptions = sagain.speaks[0]
sagainoptions.special_battle = copy.copy(enemies.steve)
sagainoptions.special_battle.lv = 5
sagain.eventrequirements = [EventRequirement("beatsteve")]

# make the boss battle force C minor
scarysteve.special_battle.specialscale = "C minor"

slose = getconversation("steveloses")
slose.area = [0,0,outside7width, outside7height]
slose.isbutton = False
slose.storyevent = "steveloseconversation"
slose.eventrequirements = [EventRequirement("steveloseconversation", -1, 1), EventRequirement("beatsteve")]
slose.reward = "C minor"

outside7.conversations = [tpboss1, animstarter, scarysteve,slose, sagain]

# tutorialwin###################################################################################

trophy = Rock("trophy", 40, 70, [0,3/4, 1, 1/4])
tutorialwin = Map(graphics.grassland(200, 200), [trophy])
tutorialwin.populate_with("flower", 1)

trophyc = getconversation("trophyc")
trophyc.area = [39, 69, GR["trophy"]["w"]+2, GR["trophy"]["h"]+2]

tutorialwin.conversations = [trophyc]
tutorialwin.exitareas = [Exit("right", False, "jeremyhome", "left", "same")]
