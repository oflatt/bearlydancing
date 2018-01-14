#!/usr/bin/python
import variables, classvar, conversations, enemies, graphics, pygame
from Animation import Animation
from graphics import scale_pure
from graphics import GR
from Map import Map
from Rock import Rock
from Exit import Exit
from pygame import Rect
from Conversation import Conversation
from Speak import Speak
from variables import displayscale, fasttestmodep

if fasttestmodep:
    from mapsvars import *
else:
    from forestmaps import *

# outside1######################################################################################
b = GR["horizontal"]["w"] / 10
housewidth = GR["honeyhouseoutside"]["w"]
househeight = GR["honeyhouseoutside"]["h"]

#stands for random pine tree
rpt = graphics.pinetree()
rgrassland = graphics.grassland(700, 500)
treerock = Rock(rpt, 3.5 * b + housewidth, 1.5 * b, treecollidesection)
meangreeny = treerock.y + GR[rpt]["h"] - GR["meangreen0"]["h"]
meangreenrock = Rock("meangreen0", treerock.x + 0.5 * b, meangreeny, [0, 0.81, 1, 0.19])

houserock = Rock("honeyhouseoutside", housewidth, 0,
                 [0,1/2,1,1/2 - (20/GR["honeyhouseoutside"]["img"].get_height())])
outside1 = Map(rgrassland,
               [houserock,
                Rock(graphics.greyrock(), 6.5 * b, 7.5 * b, variables.ROCKCOLLIDESECTION),
                treerock,
                meangreenrock])
outsidewidth = GR[rgrassland]["w"]
outsideheight = GR[rgrassland]["h"]
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
outside1c.storyrequirement = [getpartofstory("greenie")]
outside1c.storytimestalkedtogreaterthan = -1
# for tutorial, 0
enemies.greenie.lv = 0
outside1c.special_battle = enemies.greenie
outside1c.special_battle_story_penalty = 1

goodc = conversations.prettygood
goodc.area = [0,0,outsidewidth,outsideheight]
goodc.storyrequirement = [getpartofstory("good job")]
goodc.storytimestalkedtogreaterthan = -1
goodc.isbutton = False

conversations.gotoforest.area = [0,0,b/2,b*20]
conversations.gotoforest.isbutton = False
conversations.gotoforest.exitteleport = [b/2 + honeyw/4, "same"]
conversations.gotoforest.storyrequirement = [getpartofstory("greenie")]

conversations.want2go.area = [meangreenrock.x - 5, meangreenrock.y - 5, meangreenrock.w+10, meangreenrock.h+10]
enemies.greenie.lv = 1
conversations.want2gospeak.special_battle = enemies.greenie
conversations.want2go.storyrequirement = [getpartofstory("forest")]

outside1.conversations = [outside1c, conversations.gotoforest, goodc, conversations.want2go]

# letter########################################################################################
paperscale = int((variables.height/GR["paper"]["h"])/(variables.displayscale))

GR["backgroundforpaper"]["img"] = pygame.transform.scale(GR["backgroundforpaper"]["img"],
                                                         [GR["backgroundforpaper"]["w"]*paperscale,
                                                          GR["backgroundforpaper"]["h"]*paperscale])
                                                          
GR["backgroundforpaper"]["w"] *= paperscale
GR["backgroundforpaper"]["h"] *= paperscale
b = GR['backgroundforpaper']['w'] / 10

GR["paper"]["img"] = pygame.transform.scale(GR["paper"]["img"],
                                            [GR["paper"]["w"]*paperscale,
                                             GR["paper"]["h"]*paperscale])
GR["paper"]["w"] *= paperscale
GR["paper"]["h"] *= paperscale
bigpaper = Rock("paper", (GR["backgroundforpaper"]['w'] - GR["paper"]["w"]) / 2, 0, None)
bigpaper.background_range = None  # always in front
s1 = variables.font.render("I stole your lunch.", 0, variables.BLACK).convert()
s2 = variables.font.render("-Trash Panda", 0, variables.BLACK).convert()
lettertextscalefactor = (GR["paper"]['w'] * (3/4)) / s1.get_width()
s1 = pygame.transform.scale(s1, [int(lettertextscalefactor*s1.get_width()), int(lettertextscalefactor*s1.get_height())])
s2 = pygame.transform.scale(s2, [int(lettertextscalefactor*s2.get_width()), int(lettertextscalefactor*s2.get_height())])
graphics.addsurfaceGR(s1, "stolelunchtext", [s1.get_width(), s1.get_height()])
graphics.addsurfaceGR(s2, "tplunchtext", [s2.get_width(), s2.get_height()])

w1 = Rock("stolelunchtext", b * 5 - s1.get_width() / 2, b * 3, None)
w1.background_range = None
w2 = Rock("tplunchtext", b * 5 - s2.get_width() / 2, b * 4.5, None)
w2.background_range = None

letter = Map("backgroundforpaper", [bigpaper,
                                        w1,
                                        w2])

letter.playerenabledp = False

conversations.thatracoon.area = [0, 0, b * 10, b * 10]
conversations.thatracoon.storyrequirement = [getpartofstory("that racoon")]
conversations.thatracoon.storytimestalkedtogreaterthan = -1
letter.conversations = [conversations.thatracoon]
letter.exitareas = [Exit([0, 0, b * 10, b * 10], True, 'honeyhome', 'same', 'same')]

# honeyhome#####################################################################################
b = insidewidth / 10
table = Rock("table", p * 75, p * 110, None)
table.background_range = Rect(0, 110 + int(table.h / 2), 9999999, 9999999)
littleletter = Rock('letter', p * 75, p * 110, None)
littleletter.background_range = table.background_range.copy()
bed = Rock(["honeywakesup0", "honeywakesup1", "honeywakesup2", "honeywakesup3", "bed"],
           p*8, p*38, None, name = "bed")
stashlist = []
for x in range(10):
    stashname = "stash0" + str(x)
    stashlist.append(stashname)
honeyhome = Map("honeyhouseinside",
                [bed,
                 table,
                 littleletter,
                 Rock(stashlist, p * 130, p * 58, [0, 0.9, 1, 0.1], name="stash")])

outofbed = Conversation([], speaksafter = [[],[],[]], switchthisrock = "bed")
outofbed.area = [0, 0, b*20, b*20]
outofbed.storyrequirement = [getpartofstory("bed")]
outofbed.storytimestalkedtogreaterthan = len(bed.animations)-3
outofbed.showbutton = False

eatfromstash = Conversation([],
                            speaksafter = [[],[],[],[],[],[],[],[],
                                           [conversations.hungryspeak]],
                            switchthisrock="stash")

eatfromstashoffset = p*10
eatfromstash.area = [p*130+eatfromstashoffset, p*60, GR["stash00"]["w"]-2*eatfromstashoffset, GR["stash00"]["h"]]

honeyhome.conversations = [eatfromstash, outofbed]

honeyhome.startpoint = [28 * p, 39 * p]
doorexit = Exit([35 * p + honeyw / 2, 165 * p, 37 * p - honeyw, extraarea],
                True, 'outside1',
                GR["honeyhouseoutside"]["w"] * 0.3 + houserock.x, GR["honeyhouseoutside"]["h"] - honeyh + honeyfeetheight-20*p)
doorexit.conversation = conversations.hungry
doorexit.conversation.storyrequirement = [getpartofstory("letter")]

letterexit = Exit([p * 65, p * 100, 20, 30],
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
current_map_name = 'honeyhome'

# used for making the mapdict
def get_map_coded(name):
    possibles = globals()
    m = possibles.get(name)
    if not m:
        raise NotImplementedError("Map %s not implemented" % name)
    return m

def get_mapdict():
    if fasttestmodep:
        return {"honeyhome": honeyhome,"letter":letter,"outside1":outside1}
    else:
        stringlist = [home_map_name]
        maplist = [home_map]
        index = 0

        while index < len(stringlist):
            for e in maplist[index].exitareas:
                if not e.name in stringlist:
                    stringlist.append(e.name)
                    maplist.append(get_map_coded(e.name))
            index += 1
        newmapdict = {}
        
        for i in range(len(stringlist)):
            newmapdict[stringlist[i]] = maplist[i]
            
        return newmapdict

map_dict = get_mapdict()

def get_map(name):
    return map_dict[name]
    
def set_new_maps(new_mapdict):
    for key in new_mapdict:
        map_dict[key] = new_mapdict[key]

# now that everything is loaded, sort rocks ect
for key in map_dict:
    m = map_dict[key]
    if not m.isscaled:
        m.scale_stuff()
        
def new_scale_offset():
    global current_map
    variables.scaleoffset = current_map.map_scale_offset
    variables.compscale = variables.scaleoffset * variables.displayscale
    variables.compscaleunrounded = variables.scaleoffset * variables.unrounded_displayscale
    classvar.player.new_scale_offset()

def change_map_nonteleporting(name):
    global current_map_name
    global current_map
    current_map_name = name
    current_map = get_map(name)

# put player in correct place
classvar.player.teleport(current_map.startpoint[0],
                         current_map.startpoint[1])

def change_map(name, newx, newy):
    oldmapname = current_map_name
    oldplayerx = classvar.player.oldxpos
    oldplayery = classvar.player.oldypos
    
    current_map.lastx = oldplayerx
    current_map.lasty = oldplayery

    xpos = newx
    ypos = newy

    oldscaleoffset = current_map.map_scale_offset

    #now current map is the new one
    change_map_nonteleporting(name)

    halfhoneywidth = int(honeyw/2)*current_map.map_scale_offset
    halfhoneyheight = int(honeyh/2) * current_map.map_scale_offset
    # now handle newx and newy if they are a string
    if newx == "right" or newx == "r":
        xpos = GR[current_map.base]["w"] - halfhoneywidth-1
    elif newx == "left" or newx == "l":
        xpos = -halfhoneywidth+1
    if newy == "up" or newy == "u" or newy == "top" or newy == "t":
        ypos = -halfhoneyheight+1
    elif newy == "down" or newy == "bottom" or newy == "d" or newy == "b":
        ypos = GR[current_map.base]["h"]-halfhoneyheight-1

    #if the new pos is the same
    if newx == "same" or newx == "s":
        xpos = classvar.player.xpos
        xpos /= oldscaleoffset
        xpos *= current_map.map_scale_offset
        if (xpos < 0):
            xpos = 0
        if (xpos > (GR[current_map.base]["w"] * current_map.map_scale_offset - (honeyw * current_map.map_scale_offset))):
            xpos = GR[current_map.base]["w"] * current_map.map_scale_offset - (honeyw * current_map.map_scale_offset)
    else:
        xpos *= current_map.map_scale_offset

    if newy == "same" or newy == "s":
        ypos = classvar.player.ypos
        ypos /= oldscaleoffset
        ypos *= current_map.map_scale_offset
        if (ypos < 0):
            ypos = 0
        if (ypos > (GR[current_map.base]["h"] * current_map.map_scale_offset - (honeyh * current_map.map_scale_offset))):
            ypos = GR[current_map.base]["h"] * current_map.map_scale_offset - (honeyh * current_map.map_scale_offset)
    else:
        ypos *= current_map.map_scale_offset

    #for uselastposq
    if current_map.uselastposq and current_map.lastx != None:
        xpos = current_map.lastx
        ypos = current_map.lasty

    classvar.player.teleport(xpos, ypos)
    if not current_map.playerenabledp:
        classvar.player.change_of_state()
    else:
        classvar.player.soft_change_of_state()
    new_scale_offset()

    if classvar.player.collisioncheck(classvar.player.xpos, classvar.player.ypos):
        change_map_nonteleporting(oldmapname)
        classvar.player.soft_change_of_state()
        new_scale_offset()
        classvar.player.teleport(oldplayerx, oldplayery)


def engage_conversation(c):
    classvar.player.change_of_state()
    variables.settings.backgroundstate = variables.settings.state
    if variables.settings.backgroundstate == "battle":
        classvar.battle.pause()


    if not (c.storytimestalkedtogreaterthan == None and c.storytimestalkedtolessthan == None):
        lessthanp = False
        if c.storytimestalkedtolessthan == None:
            lessthanp = True
        else:
            if c.timestalkedto < c.storytimestalkedtolessthan:
                lessthanp = True

        greaterthanp = False
        if c.storytimestalkedtogreaterthan == None:
            greaterthanp = True
        else:
            if c.timestalkedto > c.storytimestalkedtogreaterthan:
                greaterthanp = True

        if lessthanp and greaterthanp:
            classvar.player.storyprogress += 1
        
    variables.settings.state = "conversation"
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

