#!/usr/bin/python
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

STORYORDER = ["bed","letter", "that racoon", "greenie", "good job", "the end"]
# a list of story parts that the player should have no control over the bear in and bear is invisible in
DISABLEPLAYERSTORY = ["bed", "that racoon"]

def getpartofstory(storyname):
    return STORYORDER.index(storyname)

def playerenabledp():
    return not STORYORDER[classvar.player.storyprogress] in DISABLEPLAYERSTORY

# Coordinates for maps are based on the base of each map respectively
honeyw = GR["honeyside0"]["w"]
honeyh = GR["honeyside0"]["h"]
honeyfeetheight = honeyh * (3 / 29)
extraarea = 50
insidewidth = GR["honeyhouseinside"]["w"]
insideheight = GR["honeyhouseinside"]["h"]
# p is the width of a pixel
p = graphics.viewfactorrounded

treecollidesection = variables.TREECOLLIDESECTION

# outside5 #####################################################################################
outside5 = Map(graphics.grassland(800, 500, downpath = True), [])
outside5.populate_with("greyrock", 4)
outside5.populate_with("pinetree", 15)
outside5.enemies = enemies.woodsenemies
outside5.lvrange = [2]
outside5.exitareas = [Exit("left", False, "outside3", "right", "same"),
                      Exit("bottom", False, "outside4", "same", "top")]

# outside4/rockorsheep##########################################################################
rgrassland = graphics.grassland(800, 500, leftpath = False, rightpath = False, uppath = True)
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
    rrockw = rrock.animations[0].pics[0]["img"].get_width()
    rrockh = rrock.animations[0].pics[0]["img"].get_height()
    sheepw = GR["sheepstanding"]["img"].get_width()
    sheeph = GR["sheepstanding"]["img"].get_height()
    return abs(rrockw-sheepw) <= sheeptorocktolerance and abs(rrockh-sheeph) <= sheeptorocktolerance
for x in range(3):
    if sheepsizep(randrock):
        break
    else:
        # if it does not fit try again
        randrock = getrandomrock()

randrock.animations.append(Animation([GR["sheepstanding"]],1))
randrock.name = "sheeprock"

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
b = rgrassland["w"] / 10
outsideheight = rgrassland["h"]
outside3 = Map(rgrassland, [])
outside3.populate_with("greyrock", 4)
outside3.populate_with("pinetree", 12)
outside3.exitareas = [Exit("bottom", False, "outside2", "same", "top"),
                      Exit("right", False, "outside5", "left", "same")]
outside3.enemies = enemies.woodsenemies
outside3.lvrange = [1, 2]

# outside2######################################################################################
rgrassland = graphics.grassland(600, 500, rightpath = False, uppath = True)
outsideheight = rgrassland["h"]
b = rgrassland["w"] / 10
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
b = rgrassland["w"]/10
hole = Rock(GR["rabbithole"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 1 / 2, 1, 1 / 2])
jmyman = Rock(GR["jeremy0"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0, 3 / 4, 1, 1 / 4])
jmyman.background_range = hole.background_range.copy()
dancelionanim = Animation([GR["dancelion0"], GR["dancelion1"]], 3000)

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

# outside1######################################################################################
b = GR["horizontal"]["w"] / 10
housewidth = GR["honeyhouseoutside"]["w"]
househeight = GR["honeyhouseoutside"]["h"]

#stands for random pine tree
rpt = graphics.pinetree()
rgrassland = graphics.grassland(700, 500)
treerock = Rock(rpt, 3.5 * b + housewidth, 1.5 * b, treecollidesection)
meangreeny = treerock.y + rpt["h"] - GR["meangreen0"]["h"]
meangreenrock = Rock(GR["meangreen0"].copy(), treerock.x + 0.5 * b, meangreeny, [0, 0.81, 1, 0.19])

houserock = Rock(GR["honeyhouseoutside"], housewidth, 0,
                 [0,1/2,1,1/2 - (20/GR["honeyhouseoutside"]["img"].get_height())])
outside1 = Map(rgrassland,
               [houserock,
                Rock(graphics.greyrock(), 6.5 * b, 7 * b, [0, 0, 1, 1]),
                treerock,
                meangreenrock])
outsidewidth = rgrassland["w"]
outsideheight = rgrassland["h"]
outside1.startpoint = [b * 8, b * 4]
outside1.exitareas = [Exit("right", False, 'outside2', "left", "same"),
                      Exit("left", False, 'jeremyhome', "right",
                           "same"),
                      Exit([housewidth * (1.5 / 5) + houserock.x, househeight * (3 / 5), housewidth * (1 / 10),
                            househeight * (1 / 5)],
                           True, 'honeyhome',
                           p * 41, insideheight - honeyh)]
outside1.lvrange = [1, 2]
outside1c = conversations.secondscene
outside1c.area = [treerock.x, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.part_of_story = getpartofstory("greenie")
outside1c.special_battle = enemies.greenie
outside1c.special_battle_story_penalty = 1

goodc = conversations.prettygood
goodc.area = [0,0,outsidewidth,outsideheight]
goodc.part_of_story = getpartofstory("good job")
goodc.isbutton = False

conversations.gotoforest.area = [0,0,b/2,b*20]
conversations.gotoforest.isbutton = False
conversations.gotoforest.exitteleport = [b/2 + honeyw/4, "same"]
conversations.gotoforest.storyrequirement = [getpartofstory("greenie")]

outside1.conversations = [outside1c, conversations.gotoforest, goodc]

# letter########################################################################################
GR["backgroundforpaper"]["img"] = pygame.transform.scale2x(GR["backgroundforpaper"]["img"])
GR["backgroundforpaper"]["w"] *= 2
GR["backgroundforpaper"]["h"] *= 2
b = GR['backgroundforpaper']['w'] / 10
GR["paper"]["img"] = pygame.transform.scale2x(GR["paper"]["img"])
GR["paper"]["w"] *= 2
GR["paper"]["h"] *= 2
bigpaper = Rock(GR["paper"], (GR["backgroundforpaper"]['w'] - GR["paper"]["w"]) / 2, 0, None)
bigpaper.background_range = None  # always in front
s1 = variables.font.render("I stole your lunch.", 0, variables.BLACK)
s2 = variables.font.render("-Trash Panda", 0, variables.BLACK)
lettertextscalefactor = (GR["paper"]['w'] * (3/4)) / s1.get_width()
s1 = pygame.transform.scale(s1, [int(lettertextscalefactor*s1.get_width()), int(lettertextscalefactor*s1.get_height())])
s2 = pygame.transform.scale(s2, [int(lettertextscalefactor*s2.get_width()), int(lettertextscalefactor*s2.get_height())])

w1 = Rock({"img": s1, "w": s1.get_width(), "h": s1.get_height()}, b * 5 - s1.get_width() / 2, b * 3, None)
w1.background_range = None
w2 = Rock({"img": s2, "w": s2.get_width(), "h": s2.get_height()}, b * 5 - s2.get_width() / 2, b * 4.5, None)
w2.background_range = None

letter = Map(GR["backgroundforpaper"], [bigpaper,
                                        w1,
                                        w2])

letter.playerenabledp = False

conversations.thatracoon.area = [0, 0, b * 10, b * 10]
conversations.thatracoon.part_of_story = getpartofstory("that racoon")
letter.conversations = [conversations.thatracoon]
letter.exitareas = [Exit([0, 0, b * 10, b * 10], True, 'honeyhome', 'same', 'same')]

# honeyhome#####################################################################################
b = insidewidth / 10
table = Rock(GR["table"], p * 75, p * 110, [0, 0.5, 1, 0.5])
littleletter = Rock(GR['letter'], p * 75, p * 110, None)
littleletter.background_range = table.background_range.copy()
bed = Rock([GR["honeywakesup0"], GR["honeywakesup1"], GR["honeywakesup2"], GR["honeywakesup3"], GR["bed"]],
           p*8, p*38, None, name = "bed")
stashlist = []
for x in range(10):
    stashname = "stash0" + str(x)
    stashlist.append(GR[stashname])
honeyhome = Map(GR["honeyhouseinside"],
                [bed,
                 table,
                 littleletter,
                 Rock(stashlist, p * 130, p * 60, [0, 0.9, 1, 0.1], name="stash")])
hungryspeak = Speak(GR["honeyside0"],["And... I'm still hungry"])

outofbed = Conversation([], speaksafter = [[],[],[]], switchthisrock = "bed")
outofbed.area = [0, 0, b*20, b*20]
outofbed.part_of_story = getpartofstory("bed")
outofbed.showbutton = False

eatfromstash = Conversation([],
                            speaksafter = [[],[],[],[],[],[],[],[],
                                           [hungryspeak]],
                            switchthisrock="stash")
eatfromstashoffset = p*10
eatfromstash.area = [p*130+eatfromstashoffset, p*60, GR["stash00"]["w"]-2*eatfromstashoffset, GR["stash00"]["h"]]

honeyhome.conversations = [eatfromstash, outofbed]

honeyhome.startpoint = [32 * p, 39 * p]
doorexit = Exit([35 * p + honeyw / 2, 165 * p, 37 * p - honeyw, extraarea],
                True, 'outside1',
                GR["honeyhouseoutside"]["w"] * (1 / 5) + houserock.x, GR["honeyhouseoutside"]["h"] - honeyh + honeyfeetheight)
doorexit.conversation = conversations.hungry
doorexit.conversation.storyrequirement = [getpartofstory("letter")]
letterexit = Exit([p * 65, p * 100, 60, 30],
                            True, 'letter',
                            GR["paper"]['w']*(3/10), 0)
letterexit.part_of_story = getpartofstory("letter")
honeyhome.exitareas = [doorexit,
                       letterexit]
honeyhome.colliderects = [Rect(0, 0, p * 31, p * 74),  # bed
                          Rect(0, 0, insidewidth, p * 48),  # wall
                          Rect(44 * p, 0, 26 * p, 60 * p),  # wardrobe
                          Rect(p * 75, p * 110 + p * 11, p * 44, p * 13)]  # table
honeyhome.uselastposq = True



# teleportation and stuff#######################################################################
home_map = honeyhome
home_map_name = "honeyhome"
current_map = home_map
current_map.scale_stuff()
current_map_name = 'honeyhome'
classvar.player.teleport(current_map.startpoint[0],
                         current_map.startpoint[1])

def get_map(name):
    possibles = globals()
    m = possibles.get(name)
    if not m:
        raise NotImplementedError("Map %s not implemented" % name)
    return m

def get_maplist():
    stringlist = [home_map_name]
    maplist = [home_map]
    index = 0

    while index < len(stringlist):
        for e in maplist[index].exitareas:
            if not e.name in stringlist:
                stringlist.append(e.name)
                maplist.append(get_map(e.name))
        index += 1
    return maplist

map_list = get_maplist()

# now that everything is loaded, scale everything
for m in map_list:
    if not m.isscaled:
        m.scale_stuff()

def new_scale_offset():
    global current_map
    variables.scaleoffset = current_map.map_scale_offset
    classvar.player.scale_by_offset()

def change_map_nonteleporting(name):
    global current_map_name
    global current_map
    current_map_name = name
    current_map = get_map(name)


def change_map(name, newx, newy):
    oldmapname = current_map_name
    oldplayerx = classvar.player.oldxpos
    oldplayery = classvar.player.oldypos
    
    current_map.lastx = classvar.player.xpos
    current_map.lasty = classvar.player.ypos

    xpos = newx
    ypos = newy

    oldscaleoffset = current_map.map_scale_offset

    #now current map is the new one
    change_map_nonteleporting(name)

    halfhoneywidth = int(honeyw/2)*current_map.map_scale_offset
    halfhoneyheight = int(honeyh/2) * current_map.map_scale_offset
    # now handle newx and newy if they are a string
    if newx == "right" or newx == "r":
        xpos = current_map.base["w"] - halfhoneywidth-1
    elif newx == "left" or newx == "l":
        xpos = -halfhoneywidth+1
    if newy == "up" or newy == "u" or newy == "top" or newy == "t":
        ypos = -halfhoneyheight+1
    elif newy == "down" or newy == "bottom" or newy == "d" or newy == "b":
        ypos = current_map.base["h"]-halfhoneyheight-1

    #if the new pos is the same
    if newx == "same" or newx == "s":
        xpos = classvar.player.xpos
        xpos /= oldscaleoffset
        xpos *= current_map.map_scale_offset
        if (xpos < 0):
            xpos = 0
        if (xpos > (current_map.base["w"] * current_map.map_scale_offset - (honeyw * current_map.map_scale_offset))):
            xpos = current_map.base["w"] * current_map.map_scale_offset - (honeyw * current_map.map_scale_offset)
    else:
        xpos *= current_map.map_scale_offset

    if newy == "same" or newy == "s":
        ypos = classvar.player.ypos
        ypos /= oldscaleoffset
        ypos *= current_map.map_scale_offset
        if (ypos < 0):
            ypos = 0
        if (ypos > (current_map.base["h"] * current_map.map_scale_offset - (honeyh * current_map.map_scale_offset))):
            ypos = current_map.base["h"] * current_map.map_scale_offset - (honeyh * current_map.map_scale_offset)
    else:
        ypos *= current_map.map_scale_offset

    #for uselastposq
    if current_map.uselastposq and current_map.lastx != None:
        xpos = current_map.lastx
        ypos = current_map.lasty

    classvar.player.teleport(xpos, ypos)
    classvar.player.soft_change_of_state()
    new_scale_offset()

    if classvar.player.collisioncheck(classvar.player.xpos, classvar.player.ypos):
        print("collide next map")
        change_map_nonteleporting(oldmapname)
        classvar.player.soft_change_of_state()
        new_scale_offset()
        classvar.player.teleport(oldplayerx, oldplayery)


def engage_conversation(c):
    classvar.player.change_of_state()
    variables.settings.backgroundstate = variables.settings.state
    if variables.settings.backgroundstate == "battle":
        classvar.battle.pause()
    if c.part_of_story == "none":
        variables.settings.state = "conversation"
        conversations.currentconversation = c
    elif c.part_of_story == classvar.player.storyprogress:
        # don't progress in story unless all the speaks for that conversation are exhausted
        if not c.speaksafter == None:
            if c.timestalkedto < len(c.speaksafter):
                classvar.player.storyprogress -= 1
        variables.settings.state = "conversation"
        classvar.player.storyprogress += 1
        conversations.currentconversation = c
    current = conversations.currentconversation

    if conversations.currentconversation.switchthisrock != None:
        current_map.changerock(conversations.currentconversation.switchthisrock)

    if len(current.speaks) == 0:
        current.exit_conversation()


def engage_exit(e):
    if not e.part_of_story == "none":
        classvar.player.storyprogress += 1
        e.part_of_story = "none"
    change_map(e.name, e.newx, e.newy)
        
def on_key(key):
    if key in variables.settings.enterkeys:
        e = current_map.checkexit()
        c = current_map.checkconversation()
        # check for conversations first
        if not c == False:
            engage_conversation(c)
        elif not e == False:
            if type(e) == Conversation:
                engage_conversation(e)
            else:
                engage_exit(e)


def checkexit():
    e = current_map.checkexit()
    if not e == False:
        if e.isbutton == False:
            engage_exit(e)


def checkconversation():
    c = current_map.checkconversation()
    if not c == False:
        if c.isbutton == False:
            engage_conversation(c)

def changerock(rockname):
    current_map.changerock(rockname)

