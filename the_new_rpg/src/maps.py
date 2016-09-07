#!/usr/bin/python
import variables, classvar, conversations
from graphics import GR
from Map import Map
from Rock import Rock
from Exit import Exit
from Enemy import Enemy
from pygame import Rect

block = variables.width/10

houserock = Rock(GR["house"], 0, 0, False)
houserock.collideh = GR["house"]["scale-height"] * (3/5)
honeyw = GR["honeyside0"]["scale-width"]
honeyh = GR["honeyside0"]["scale-height"]

# outside 1
outside1 = Map(GR["horizontal"], [houserock,
                                  Rock(GR["meangreen0"], 3.2*block, 0.1*block+GR["talltree"]["scale-height"]-GR["meangreen0"]["scale-height"], True),
                                  Rock(GR["rock"], 6.5*block, 7*block, True),
                                  Rock(GR["rock"], 4.5*block, 3.5*block, True),
                                  Rock(GR["rock"], 2.5*block, 6.3*block, True)])
outside1scale = outside1.map_scale_offset
housewidth = int(GR["house"]["scale-width"]*outside1scale)
househeight = int(GR["house"]["scale-height"]*outside1scale)
outsidewidth = GR["horizontal"]["scale-width"]
outsideheight = GR["horizontal"]["scale-height"]
outside1.startpoint= [block*8,block*4]
outside1.exitareas = [Exit([outsidewidth, 0, 100, outsideheight], False, 'outside2', 0, block*5),
                      Exit([housewidth*(1/5), househeight*(3/5), housewidth*(1.5/10), househeight*(2/5)], True, 'honeyhome', block*5-(honeyw/2), block*10-(honeyh))]
outside1.enemies = [Enemy(GR["sheep0"], 0.5, "sheep"), Enemy(GR["meangreen0"], 0.3, "greenie"), Enemy(GR["purpleperp0"], 0.2, "purpur")]
outside1.colliderects = [Rect(0, 0, housewidth, househeight-int(honeyh*outside1scale))]
outside1.lvrange = [1,1]
outside1c = conversations.secondscene
outside1c.area = [3.1*block, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.part_of_story = 2
greenie = Enemy(GR["meangreen0"],0.3, "Greenie Meanie")
greenie.lv = 1
outside1c.special_battle = Enemy(GR["meangreen0"], 1, "Greenie Meanie")
outside1.conversations = [outside1c]
outside1.foreground_terrain = [Rock(GR["talltree"], 2.9*block, 0.1*block, False)]


#honeyhome
insidewidth = GR["bearhome"]["scale-width"]
insideheight = GR["bearhome"]["scale-height"]
insideb = insidewidth/10
honeyhome = Map(GR["bearhome"], [Rock(GR["welcomematt"],
                                      (insidewidth/2-GR["welcomematt"]["scale-width"]/2),
                                      (insideheight-GR["welcomematt"]["scale-height"]),
                                      False),
                                 Rock(GR["bed"], 0*insideb, 0*insideb, False),
                                 Rock(GR["wardrobe1"], 2*insideb, 0*insideb, False),
                                 Rock(GR["tp"], 8*insideb, 7*insideb, True)])

honeyhome.startpoint = [0,0]
honeyhome.exitareas = [Exit([insidewidth/2-GR["welcomematt"]["scale-width"]/2, insideheight,
                             GR["welcomematt"]["scale-width"], insideb], False, 'outside1', househeight, househeight)]
racoonc = conversations.firstscene
racoonc.area = [0, 7*insideb+GR["tp"]["scale-height"], insidewidth, 50]#50 because it does not matter how thick it is down
racoonc.isbutton = False
racoonc.part_of_story = 1 #makes it so you can only have the conversation once
honeyhome.conversations = [racoonc]

#outside2
outside2 = Map(GR["leftturn"], [Rock(GR["talltree"], 4*block, 5*block, True),
                                Rock(GR["talltree"], 5.5*block, 4.5*block, True),
                                Rock(GR["talltree"], 2*block, 4.7*block, True),
                                Rock(GR["talltree"], 6.7*block, 2*block, True),
                                Rock(GR["rock"], 5*block, 4*block, False),
                                Rock(GR["talltree"], 1.7*block, 0.3*block, True),
                                Rock(GR["rock"], 6*block, 2*block, True)])

outside2.exitareas = [Exit([0, 0, 5, outsideheight], False, 'outside1', outsidewidth-50, outsideheight/2),
                      Exit([0, 0, outsidewidth, 5], False, 'outside3', outsidewidth/2, outsideheight-50)]
outside2.enemies = [Enemy(GR["sheep0"], 0.5, "sheep"), Enemy(GR["meangreen0"], 0.3, "greenie"), Enemy(GR["purpleperp0"], 0.2, "purpur")]
outside2.lvrange = [1, 2]

#outside3
outside3 = Map(GR["rightturn"], [Rock(GR["talltree"], 1*block, 4*block, True),
                                 Rock(GR["rock"], 5.7*block, 7*block, True)])
outside3.foreground_terrain= [Rock(GR["talltree"], 6*block, 4*block, False)]

outside3.enemies = [Enemy(GR["ruderoo0"], 0.5, "rudaroo"), Enemy(GR["slimedog0"], 0.3, "slime dog"), Enemy(GR["pinkfly0"], 0.2, "pink fly")]
outside3.lvrange = [3, 4]
outside3.startpoint=[0,0]
outside3.exitareas = [Exit([0,outsideheight, outsidewidth, 5], False, 'outside2', outsidewidth/2, block*0.1)]

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
    classvar.player.teleport(newx*current_map.map_scale_offset, newy*current_map.map_scale_offset)
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