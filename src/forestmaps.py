import variables, classvar, conversations, enemies, graphics, random, pygame
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

from mapsvars import *

# outside5 #####################################################################################
outside5 = Map(graphics.grassland(800, 500, downpath = True), [])
outside5.populate_with("greyrock", 4)
outside5.populate_with("pinetree", 15)
outside5.enemies = enemies.woodsenemies
outside5.lvrange = [2]
outside5.exitareas = [Exit("left", False, "outside3", "right", "same"),
                      Exit("bottom", False, "outside4", "same", "top")]

# outside4/rockorsheep##########################################################################
outside4width = 800
outside4height = 500
rgrassland = graphics.grassland(outside4width, outside4height, leftpath = False, rightpath = False, uppath = True)

def make_rock_or_sheep_rocks():
    bigx = int(outside4width/2) - randint(int(outside4width/20), int(outside4width/4))
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

sheepconversation = conversations.sheepconversation
sheepconversation.area = [randrock.x, randrock.y, randrock.w, randrock.h]
sheepconversation.special_battle = enemies.sheep
sheepconversation.special_battle.lv = 3

outside4.conversations = [sheepconversation]

outside4.exitareas = [Exit("up", False, "outside5", "same", "bottom")]
outside4.enemies = enemies.woodsenemies
outside4.lvrange = [2,3]

# outside3######################################################################################
rgrassland = graphics.grassland(600, 500, leftpath = False, downpath = True)
b = GR[rgrassland]["w"] / 10
outsideheight = GR[rgrassland]["h"]
outside3 = Map(rgrassland, [])
outside3.populate_with("greyrock", 4)
outside3.populate_with("pinetree", 12)
outside3.exitareas = [Exit("bottom", False, "outside2", "same", "top"),
                      Exit("right", False, "outside5", "left", "same")]
outside3.enemies = enemies.woodsenemies
outside3.lvrange = [1, 2]

# outside2######################################################################################
rgrassland = graphics.grassland(600, 500, rightpath = False, uppath = True)
outsideheight = GR[rgrassland]["h"]
b = GR[rgrassland]["w"] / 10
outside2 = Map(rgrassland, [])
outside2.populate_with("pinetree", 22)
outside2.populate_with("greyrock", 3)

outside2.exitareas = [
    Exit("left", False, 'outside1', "right", "same"),
    Exit("top", False, 'outside3', "same", "bottom")]
outside2.enemies = enemies.woodsenemies
outside2.lvrange = [1]

# jeremyhome####################################################################################
rgrassland = graphics.grassland(800, 500)
b = GR[rgrassland]["w"]/10
hole = Rock("rabbithole", b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 1 / 2, 1, 1 / 2])
jmyman = Rock("jeremy0", b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 3 / 4, 1, 1 / 4])
jmyman.background_range = hole.background_range.copy()
dancelionanim = Animation(["dancelion0", "dancelion1"], 3000)

jeremyhome = Map(rgrassland, [hole,
                              jmyman,
                              Rock(dancelionanim, b/2, b * 4, [0, 3 / 4, 1, 1 / 4])])
jeremyhome.exitareas = [Exit("right", False, 'outside1', "left", "same")]
conversations.jeremy.area = [b * 5 + GR["rabbithole"]["w"] - (honeyw / 2), b * 5 - GR["rabbithole"]["h"],
                             GR["rabbithole"]["w"] - (honeyw / 2), GR["rabbithole"]["h"]]
conversations.dancelionpass.area = [0, 0, b, b * 10]
conversations.dancelionpass.isbutton = False
conversations.dancelionpass.exitteleport = [b + honeyw / 4, "same"]
jeremyhome.conversations = [conversations.jeremy, conversations.dancelionpass]
