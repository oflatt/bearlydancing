#!/usr/bin/python
import variables, classvar, conversations
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
print(variables.width)

# jeremyhome#############################################################################################################
b = GR["halfpath"]["w"] / 10

jeremyhome = Map(GR["horizontal"],
                 [Rock(GR["rabbithole"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], True),
                  Rock(GR["jeremy0"], b * 5 + GR["rabbithole"]["w"], b * 5 - GR["rabbithole"]["h"], True)])
jeremyhome.exitareas = [Exit([b * 10, 0, extraarea, GR["halfpath"]["h"]], False, 'outside1', 0, "same")]

# outside1##############################################################################################################
b = GR["horizontal"]["w"] / 10

outside1 = Map(GR["horizontal"], [Rock(GR["house"], 0, 0, False),
                                  Rock(GR["meangreen0"], 3.2 * b,
                                       0.1 * b + GR["talltree"]["h"] - GR["meangreen0"]["h"],
                                       True),
                                  Rock(GR["rock"], 6.5 * b, 7 * b, True),
                                  Rock(GR["rock"], 4.5 * b, 3.5 * b, True),
                                  Rock(GR["rock"], 2.5 * b, 6.3 * b, True)])
housewidth = int(GR["house"]["w"])
househeight = int(GR["house"]["h"])
outsidewidth = GR["horizontal"]["w"]
outsideheight = GR["horizontal"]["h"]
outside1.startpoint = [b * 8, b * 4]
outside1.exitareas = [Exit([outsidewidth, 0, extraarea, outsideheight], False, 'outside2', 0, "same"),
                      Exit([-extraarea, 0, extraarea, outsideheight], False, 'jeremyhome', GR["halfpath"]["w"] - honeyw,
                           "same"),
                      Exit(
                          [housewidth * (1 / 5), househeight * (3 / 5), housewidth * (1.5 / 10), househeight * (1 / 5)],
                          True, 'honeyhome',
                          (GR["bearhome"]["w"] / 2) - (honeyw / 2), GR["bearhome"]["h"] - (honeyh)-b/20)]
# outside1.colliderects = [Rect(0, 0, housewidth, househeight - honeyh)]
outside1.lvrange = [1, 1]
outside1c = conversations.secondscene
outside1c.area = [3.1 * b, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.part_of_story = 2
greenie = Enemy(GR["meangreen0"], 0.3, "Greenie Meanie")
greenie.lv = 1
outside1c.special_battle = Enemy(GR["meangreen0"], 1, "Greenie Meanie")
outside1.conversations = [outside1c]
outside1.foreground_terrain = [Rock(GR["talltree"], 2.9 * b, 0.1 * b, False)]

# honeyhome#############################################################################################################
insidewidth = GR["bearhome"]["w"]
insideheight = GR["bearhome"]["h"]
b = insidewidth / 10

honeyhome = Map(GR["bearhome"], [Rock(GR["welcomematt"],
                                      (insidewidth / 2 - GR["welcomematt"]["w"] / 2),
                                      (insideheight - GR["welcomematt"]["h"]),
                                      False),
                                 Rock(GR["bed"], 0, 0, False),
                                 Rock(GR["wardrobe1"], 2 * b, 0 * b, False),
                                 Rock(GR["tp"], 8 * b, 7 * b, True)])
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

# houserock = Rock(GR["house"], 0, 0, False)
# houserock.collideh = GR["house"]["h"] * (3/5)
# honeyw = GR["honeyside0"]["w"]
# honeyh = GR["honeyside0"]["h"]
#
# outside1 = Map(GR["horizontal"], [houserock,
#                                   Rock(GR["meangreen0"], 3.2*block, 0.1*block+GR["talltree"]["h"]-GR["meangreen0"]["h"], True),
#                                   Rock(GR["rock"], 6.5*block, 7*block, True),
#                                   Rock(GR["rock"], 4.5*block, 3.5*block, True),
#                                   Rock(GR["rock"], 2.5*block, 6.3*block, True)])
# outside1scale = outside1.map_scale_offset
# housewidth = int(GR["house"]["w"]*outside1scale)
# househeight = int(GR["house"]["h"]*outside1scale)
# outsidewidth = GR["horizontal"]["w"]
# outsideheight = GR["horizontal"]["h"]
# outside1.startpoint= [block*8,block*4]
# outside1.exitareas = [Exit([outsidewidth, 0, 100, outsideheight], False, 'outside2', 0, block*5),
#                       Exit([housewidth*(1/5), househeight*(3/5), housewidth*(1.5/10), househeight*(2/5)], True, 'honeyhome',
#                            (GR["bearhome"]["w"]/5)-(honeyw/2), GR["bearhome"]["h"]-(honeyh))]
# outside1.enemies = [Enemy(GR["sheep0"], 0.5, "sheep"), Enemy(GR["meangreen0"], 0.3, "greenie"), Enemy(GR["purpleperp0"], 0.2, "purpur")]
# outside1.colliderects = [Rect(0, 0, housewidth, househeight-int(honeyh*outside1scale))]
# outside1.lvrange = [1,1]
# outside1c = conversations.secondscene
# outside1c.area = [3.1*block, 0, outsidewidth, outsideheight]
# outside1c.isbutton = False
# outside1c.part_of_story = 2
# greenie = Enemy(GR["meangreen0"],0.3, "Greenie Meanie")
# greenie.lv = 1
# outside1c.special_battle = Enemy(GR["meangreen0"], 1, "Greenie Meanie")
# outside1.conversations = [outside1c]
# outside1.foreground_terrain = [Rock(GR["talltree"], 2.9*block, 0.1*block, False)]
#
#
# #honeyhome
# insidewidth = GR["bearhome"]["w"]
# insideheight = GR["bearhome"]["h"]
# insideb = insidewidth/10
# honeyhome = Map(GR["bearhome"], [Rock(GR["welcomematt"],
#                                       (insidewidth/2-GR["welcomematt"]["w"]/2),
#                                       (insideheight-GR["welcomematt"]["h"]),
#                                       False),
#                                  Rock(GR["bed"], 0*insideb, 0*insideb, False),
#                                  Rock(GR["wardrobe1"], 2*insideb, 0*insideb, False),
#                                  Rock(GR["tp"], 8*insideb, 7*insideb, True)])
#
# honeyhome.startpoint = [0,0]
# honeyhome.exitareas = [Exit([insidewidth/2-GR["welcomematt"]["w"]/2, insideheight,
#                              GR["welcomematt"]["w"], insideb], False, 'outside1',
#                              GR["house"]["w"]*(1/5), GR["house"]["h"]-honeyh)]
# racoonc = conversations.firstscene
# racoonc.area = [0, 7*insideb+GR["tp"]["h"], insidewidth, extraarea]#extraarea because it does not matter how thick it is down
# racoonc.isbutton = False
# racoonc.part_of_story = 1 #makes it so you can only have the conversation once
# honeyhome.conversations = [racoonc]
#
# #outside2
# outside2 = Map(GR["leftturn"], [Rock(GR["talltree"], 4*block, 5*block, True),
#                                 Rock(GR["talltree"], 5.5*block, 4.5*block, True),
#                                 Rock(GR["talltree"], 2*block, 4.7*block, True),
#                                 Rock(GR["talltree"], 6.7*block, 2*block, True),
#                                 Rock(GR["rock"], 5*block, 4*block, False),
#                                 Rock(GR["talltree"], 1.7*block, 0.3*block, True),
#                                 Rock(GR["rock"], 6*block, 2*block, True)])
#
# outside2.exitareas = [Exit([0, 0, 5, outsideheight], False, 'outside1', outsidewidth-extraarea, outsideheight/2),
#                       Exit([0, 0, outsidewidth, 5], False, 'outside3', outsidewidth/2, outsideheight-extraarea)]
# outside2.enemies = [Enemy(GR["sheep0"], 0.5, "sheep"), Enemy(GR["meangreen0"], 0.3, "greenie"), Enemy(GR["purpleperp0"], 0.2, "purpur")]
# outside2.lvrange = [1, 2]
#
# #outside3
# outside3 = Map(GR["rightturn"], [Rock(GR["talltree"], 1*block, 4*block, True),
#                                  Rock(GR["rock"], 5.7*block, 7*block, True)])
# outside3.foreground_terrain= [Rock(GR["talltree"], 6*block, 4*block, False)]
#
# outside3.enemies = [Enemy(GR["ruderoo0"], 0.5, "rudaroo"), Enemy(GR["slimedog0"], 0.3, "slime dog"), Enemy(GR["pinkfly0"], 0.2, "pink fly")]
# outside3.lvrange = [3, 4]
# outside3.startpoint=[0,0]
# outside3.exitareas = [Exit([0,outsideheight, outsidewidth, 5], False, 'outside2', outsidewidth/2, block*0.1)]

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
            print("tried newy :" + str(newy))
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
