#!/usr/bin/python
import variables, classvar, conversations, pygame
from graphics import GR
from Map import Map
from Rock import Rock
from Exit import Exit
from Enemy import Enemy
from pygame import Rect

# Coordinates for maps are based on the base of each map respectively
honeyw = GR["honeyside0"]["w"]
honeyh = GR["honeyside0"]["h"]
extraarea = 50

# outside3##############################################################################################################
b = GR["rightturn"]["w"]/10
outsideheight = GR["rightturn"]["h"]
outside3 = Map(GR["rightturn"], [])
outside3.exitareas = [Exit([0, outsideheight, b*10, extraarea], False, "outside2", "same", 0)]

# outside2##############################################################################################################
b = GR["leftturn"]["w"]/10
outsideheight = GR["leftturn"]["h"]
outside2 = Map(GR["leftturn"], [Rock(GR["talltree"], 4*b, 5*b, [0,0,1,1]),
                                Rock(GR["talltree"], 5.5*b, 4.5*b, [0,0,1,1]),
                                Rock(GR["talltree"], 2*b, 4.7*b, [0,0,1,1]),
                                Rock(GR["talltree"], 6.7*b, 2*b, [0,0,1,1]),
                                Rock(GR["rock"], 5*b, 4*b, [0,0,1,1]),
                                Rock(GR["talltree"], 1.7*b, 0.3*b, [0,0,1,1]),
                                Rock(GR["rock"], 6*b, 2*b, [0,0,1,1])])

outside2.exitareas = [Exit([-extraarea, 0, extraarea, outsideheight], False, 'outside1', GR["horizontal"]["w"] - honeyw, "same")]
outside2.enemies = [Enemy(GR["sheep0"], 0.5, "sheep", []),
                    Enemy(GR["meangreen0"], 0.3, "greenie", ["skippy"]),
                    Enemy(GR["purpleperp0"], 0.2, "purpur", [])]
outside2.lvrange = [2,3]

# jeremyhome############################################################################################################
b = GR["halfpath"]["w"] / 10

jeremyhome = Map(GR["horizontal"],
                 [Rock(GR["rabbithole"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0,0,1,1]),
                  Rock(GR["jeremy0"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], [0,0,1,1])])
jeremyhome.exitareas = [Exit([b * 10, int(GR["house"]["h"]), extraarea, GR["halfpath"]["h"]], False, 'outside1', 0, "same")]
conversations.jeremy.area = [b * 5 + GR["rabbithole"]["w"]-(honeyw/2), b * 5 - GR["rabbithole"]["h"],
                             GR["rabbithole"]["w"]-(honeyw/2), GR["rabbithole"]["h"]]
jeremyhome.conversations = [conversations.jeremy]

# outside1##############################################################################################################
b = GR["horizontal"]["w"] / 10

treerock = Rock(GR["talltree"], 2.9 * b, 0.1 * b, None)
meangreany = 0.1 * b + GR["talltree"]["h"] - GR["meangreen0"]["h"]
outside1 = Map(GR["horizontal"], [Rock(GR["house"], 0, 0, None),
                                  Rock(GR["meangreen0"], 3.2 * b,
                                       meangreany,
                                       [0,0,1,1]),
                                  Rock(GR["rock"], 6.5 * b, 7 * b, [0,0,1,1]),
                                  Rock(GR["rock"], 4.5 * b, 3.5 * b, [0,0,1,1]),
                                  Rock(GR["rock"], 2.5 * b, 6.3 * b, [0,0,1,1]),
                                  treerock])
housewidth = int(GR["house"]["w"])
househeight = int(GR["house"]["h"])
outsidewidth = GR["horizontal"]["w"]
outsideheight = GR["horizontal"]["h"]
outside1.startpoint = [b * 8, b * 4]
outside1.exitareas = [Exit([outsidewidth, 0, extraarea, outsideheight], False, 'outside2', 0, "same"),
                      Exit([-extraarea, 0, extraarea, outsideheight], False, 'jeremyhome', GR["halfpath"]["w"] - honeyw,
                           "same"),
                      Exit(
                          [housewidth * (1.5 / 5), househeight * (3 / 5), housewidth * (1 / 10), househeight * (1 / 5)],
                          True, 'honeyhome',
                          (GR["bearhome"]["w"] / 2) - (honeyw / 2), GR["bearhome"]["h"] - (honeyh)-b/20)]
outside1.colliderects = [Rect(0, 0, housewidth, househeight - honeyh)]
outside1.lvrange = [1, 2]
outside1c = conversations.secondscene
outside1c.area = [3.1 * b, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.part_of_story = 2
outside1c.special_battle = Enemy(GR["meangreen0"], 1, "Greenie Meanie", ["skippy"])
outside1.conversations = [outside1c]

# honeyhome#############################################################################################################
insidewidth = GR["bearhome"]["w"]
insideheight = GR["bearhome"]["h"]
b = insidewidth / 10

honeyhome = Map(GR["bearhome"], [Rock(GR["welcomematt"],
                                      (insidewidth / 2 - GR["welcomematt"]["w"] / 2),
                                      (insideheight - GR["welcomematt"]["h"]),
                                      None),
                                 Rock(GR["bed"], 0, 0, None),
                                 Rock(GR["wardrobe1"], 2 * b, 0 * b, None),
                                 Rock(GR["tp"], 8 * b, 7 * b, [0,3/4,1,1/4])])
honeyhome.startpoint = [0, 0]
honeyhome.exitareas = [
    Exit([insidewidth / 2 - GR["welcomematt"]["w"] / 2, insideheight, GR["welcomematt"]["w"] / 2, extraarea],
         False, 'outside1',
         GR["house"]["w"] * (1 / 5), GR["house"]["h"] - honeyh)]
racoonc = conversations.firstscene
racoonc.area = [0, 7 * b + GR["tp"]["h"], insidewidth,
                extraarea]  # extraarea because it does not matter how thick it is down
racoonc.isbutton = False
racoonc.part_of_story = 1  # makes it so you can only have the conversation once
honeyhome.conversations = [racoonc]
#collide with two walls
honeyhome.colliderects = [Rect(0, b*2.7, b*2.1, b*1.5), Rect(b*(10-2.3), b*2.7, b*2.3, b*1.5),
                          Rect(2*b+(b/2), 0, GR["wardrobe1"]["w"]-b, GR["wardrobe1"]["h"]/10)]


# teleportation and stuff###############################################################################################
current_map = honeyhome
home_map = ('honeyhome')
classvar.player.teleport(current_map.startpoint[0], current_map.startpoint[1])


def new_scale_offset():
    global current_map
    variables.scaleoffset = current_map.map_scale_offset
    classvar.player.scale_by_offset()


def change_map(name, newx, newy):
    global current_map
    possibles = globals()
    map_picked = possibles.get(name)
    if not map_picked:
        raise NotImplementedError("Map %s not implemented" % name)
    current_map = map_picked
    if (isinstance(newx, str)):
        newx = classvar.player.xpos
        if (newx < 0):
            newx = 0
        if (newx > (current_map.base["w"]*current_map.map_scale_offset - (honeyw * current_map.map_scale_offset))):
            newx = current_map.base["w"]*current_map.map_scale_offset - (honeyw * current_map.map_scale_offset)
    else:
        newx *= current_map.map_scale_offset
    if (isinstance(newy, str)):
        newy = classvar.player.ypos
        if (newy < 0):
            newy = 0
        if (newy > (current_map.base["h"]*current_map.map_scale_offset - (honeyh * current_map.map_scale_offset))):
            newy = current_map.base["h"]*current_map.map_scale_offset - (honeyh * current_map.map_scale_offset)
    else:
        newy *= current_map.map_scale_offset
    classvar.player.teleport(newx, newy)
    new_scale_offset()


def engage_conversation(c):
    classvar.player.change_of_state()
    if c.part_of_story == "none":
        variables.state = "conversation"
        conversations.currentconversation = c
    elif c.part_of_story == classvar.player.storyprogress:
        variables.state = "conversation"
        classvar.player.storyprogress += 1
        conversations.currentconversation = c


def on_key(key):
    if key in variables.enterkeys:
        e = current_map.checkexit()
        c = current_map.checkconversation()
        if not e == False:
            change_map(e.name, e.newx, e.newy)
        elif not c == False:
            engage_conversation(c)


def checkexit():
    e = current_map.checkexit()
    if not e == False:
        if e.isbutton == False:
            change_map(e.name, e.newx, e.newy)


def checkconversation():
    c = current_map.checkconversation()
    if not c == False:
        if c.isbutton == False:
            engage_conversation(c)
