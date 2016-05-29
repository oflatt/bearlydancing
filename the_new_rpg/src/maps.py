#!/usr/bin/python
import pygame, variables, graphics, classvar, conversations
from Map import Map
from Rock import Rock
from Exit import Exit
from Enemy import Enemy
s = variables.scaleoffset

block = variables.width/10

houserock = Rock(graphics.house, 0, 0, True)
houserock.h = houserock.h * (3/5)
housewidth = graphics.house["scale-width"]

# outside 1
outside1 = Map(graphics.scrub1, [houserock,
                                 Rock(graphics.tree3, 1.4*block, 1.9*block, True),
                                 Rock(graphics.sheep1, 1.1*block, 7.3*block, False),
                                 Rock(graphics.meanGreen0, 3*block, 2.5*block, False),
                                 Rock(graphics.purplePerp0, 8*block, 5.3*block, False),
                                 Rock(graphics.rock, 6.5*block, 7*block, True),
                                 Rock(graphics.rock, 4.5*block, 3.5*block, False),
                                 Rock(graphics.tree3, 1.9*block, 1.9*block, True),
                                 Rock(graphics.tree3, 2.4*block, 1.9*block, True),
                                 Rock(graphics.tall_Tree, 3.3*block, 6.7*block, True),
                                 Rock(graphics.tall_Tree, 4.5*block, 5.3*block, True),
                                 Rock(graphics.tall_Tree2, 0.5*block, 4.5*block, True),
                                 Rock(graphics.tall_Tree, 2.9*block, 0.1*block, True),
                                 Rock(graphics.tall_Tree2, 5.2*block, 8, True),
                                 Rock(graphics.tall_Tree2, 7.8*block, 8, True),
                                 Rock(graphics.tall_Tree, 7.9*block, 5.3*block, True),
                                 Rock(graphics.rock, 2.5*block, 6.3*block, True)])

outsidewidth = graphics.scrub1["scale-width"]
outsideheight = graphics.scrub1["scale-height"]
outside1.startpoint= [block*8,block*4]
outside1.exitareas = [Exit([outsidewidth, 0, 100, outsideheight], False, 'outside2', 25, outsideheight/2),
                      Exit([housewidth*(1/5), housewidth*(3/5), housewidth*(1/5), housewidth*(3/32)], True, 'honeyhome', block*4.3, block*8 )]
outside1.enemies = [Enemy(graphics.sheep1, 0.5, "sheep"), Enemy(graphics.meanGreen0, 0.3, "greenie"), Enemy(graphics.purplePerp0, 0.2, "purpur")]
outside1.lvrange = [1,1]
outside1c = conversations.secondscene
outside1c.area = [3.1*block, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.part_of_story = 2
greenie = Enemy(graphics.meanGreen0,0.3, "Greenie Meanie")
greenie.lv = 1
outside1c.special_battle = Enemy(graphics.meanGreen0, 1, "Greenie Meanie")
outside1.conversations = [outside1c]


#honeyhome
insidewidth = graphics.houseInside["scale-width"]
insideheight = graphics.houseInside["scale-height"]
insideb = insidewidth/10
honeyhome = Map(graphics.houseInside, [Rock(graphics.welcomeMat,
                                            (insidewidth/2-graphics.welcomeMat["scale-width"]/2),
                                            (insideheight-graphics.welcomeMat["scale-height"]),
                                            False),
                                       Rock(graphics.bed, 0*insideb, 0*insideb, False),
                                       Rock(graphics.warddrobe2, 2*insideb, 0*insideb, False),
                                       Rock(graphics.tpanda, 8*insideb, 7*insideb, False)])

honeyhome.startpoint = [0,0]
honeyhome.exitareas = [Exit([insidewidth/2-graphics.welcomeMat["scale-width"]/2, insideheight,
                             graphics.welcomeMat["scale-width"], insideb], False, 'outside1', insideb*0.9, insideb*4)]
racoonc = conversations.firstscene
racoonc.area = [0, 7*insideb, insidewidth, 50]#50 because it does not matter how thick it is down
racoonc.isbutton = False
racoonc.part_of_story = 1 #makes it so you can only have the conversation once
honeyhome.conversations = [racoonc]

#outside2
outside2 = Map(graphics.leftTurn, [Rock(graphics.tall_Tree, 4*block, 5*block, True),
                                   Rock(graphics.tall_Tree2, 5.5*block, 4.5*block, True),
                                   Rock(graphics.tall_Tree, 2*block, 4.7*block, True),
                                   Rock(graphics.tall_Tree2, 6.7*block, 2*block, True),
                                   Rock(graphics.rock, 5*block, 4*block, False),
                                   Rock(graphics.tall_Tree, 1.7*block, 0.3*block, True),
                                   Rock(graphics.rock, 6*block, 2*block, True)])

outside2.exitareas = [Exit([0, 0, 5, outsideheight], False, 'outside1', outsidewidth-50, outsideheight/2),
                      Exit([0, 0, outsidewidth, 5], False, 'outside3', outsidewidth/2, outsideheight-50)]
outside2.enemies = [Enemy(graphics.sheep1, 0.5, "sheep"), Enemy(graphics.meanGreen0, 0.3, "greenie"), Enemy(graphics.purplePerp0, 0.2, "purpur")]
outside2.lvrange = [1, 2]

#outside3
outside3 = Map(graphics.rightTurn, [Rock(graphics.tall_Tree, 1*block, 4*block, True),
                                    Rock(graphics.rock, 5.7*block, 7*block, True)])
outside3.foreground_terrain= [Rock(graphics.tall_Tree, 6*block, 4*block, False)]

outside3.enemies = [Enemy(graphics.ruderoo0, 0.5, "rudaroo"), Enemy(graphics.slime_dog, 0.3, "slime dog"), Enemy(graphics.pink_fly, 0.2, "pink_fly")]
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

def change_map(name):
    global current_map
    if name == "honeyhome":
        current_map = honeyhome
    if name == 'outside1':
        current_map = outside1
    if name == "outside2":
        current_map = outside2
    if name == "outside3":
        current_map = outside3
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
            classvar.player.teleport(e.newx, e.newy)
            change_map(e.name)
        elif not c == False:
            engage_conversation(c)

def checkexit():
    e = current_map.checkexit()
    if not e == False:
        if e.isbutton == False:
            classvar.player.teleport(e.newx, e.newy)
            change_map(e.name)

def checkconversation():
    c = current_map.checkconversation()
    if not c == False:
        if c.isbutton == False:
            engage_conversation(c)