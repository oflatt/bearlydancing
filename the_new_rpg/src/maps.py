#!/usr/bin/python
import pygame, variables, graphics, classvar, conversations
from Map import Map
from Rock import Rock
from Exit import Exit
from Enemy import Enemy
s = variables.scaleoffset

block = variables.width/10
testmap1 = Map(graphics.testmapimage, [Rock(graphics.bed, 2*block, 2*block, True),
                                       Rock(graphics.bed, 3*block, 2*block, True),
                                       Rock(graphics.front_honey, 6*block, 2*block, False)])
testmap1.startpoint = [block * 10, block*10]

houserock = Rock(graphics.house, 0, 0, True)
houserock.h = houserock.h * (3/5)
housewidth = graphics.house.get_width()

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
                                 Rock(graphics.tall_Tree2, 7.5*block, 8, True),
                                 Rock(graphics.tall_Tree, 8.2*block, 5.3*block, True),
                                 Rock(graphics.rock, 2.5*block, 6.3*block, True)])

outsidewidth = graphics.scrub1.get_width()
outsideheight = graphics.scrub1.get_height()
outside1.startpoint= [block*8,block*4]
outside1.exitareas = [Exit([outsidewidth, 0, 100, outsideheight], False, 'outside2', 0, block*4),
                      Exit([housewidth*(1/5), housewidth*(3/5), housewidth*(1/5), housewidth*(3/32)], True, 'honeyhome', 0, 0)]
outside1.enemies = [Enemy(graphics.sheep1, 0.9, "sheep"), Enemy(graphics.meanGreen0, 0.7, "greenie"), Enemy(graphics.purplePerp0, 0.5, "purpur")]
outside1.lvrange = [1, 2]
outside1.conversations = [conversations.testconversation]

#honeyhome
insidewidth = graphics.houseInside.get_width()
insideheight = graphics.houseInside.get_height()
insideb = insidewidth/10
honeyhome = Map(graphics.houseInside, [Rock(graphics.welcomeMat,
                                            (insidewidth/2-graphics.welcomeMat.get_width()/2),
                                            (insideheight-graphics.welcomeMat.get_height()),
                                            False),
                                       Rock(graphics.bed, 0*insideb, 0*insideb, False),
                                       Rock(graphics.warddrobe2, 2*insideb, 0*insideb, False),
                                       Rock(graphics.tpanda, 8*insideb, 7*insideb, False),
                                       Rock(graphics.wiiu, 5*insideb, 0.1*insideb, False)])

honeyhome.startpoint = [0,0]
honeyhome.exitareas = [Exit([insidewidth/2-graphics.welcomeMat.get_width()/2, insideheight,
                             graphics.welcomeMat.get_width(), insideb], False, 'outside1', insideb*0.85, insideb*6)]
racoonc = conversations.firstscene
racoonc.area = [0, 7*insideb, insidewidth, 50]#50 because it does not matter how thick it is down
racoonc.isbutton = False
racoonc.part_of_story = 1 #makes it so you can only have the conversation once
honeyhome.conversations = [racoonc]

outside2 = Map(graphics.leftTurn, [Rock(graphics.tall_Tree, 4*block, 5*block, True),
                                   Rock(graphics.tall_Tree2, 5.5*block, 4.5*block, True),
                                   Rock(graphics.tall_Tree, 2*block, 4.7*block, True),
                                   Rock(graphics.tall_Tree2, 6.7*block, 2*block, True),
                                   Rock(graphics.rock, 5*block, 4*block, False),
                                   Rock(graphics.tall_Tree, 1.7*block, 0.3*block, True)])

outside2.exitareas = [Exit([outsidewidth, outsideheight, 0, 100], False, 'outside1', 4*block, 4*block)]
outside2.enemies = [Enemy(graphics.sheep1, 0.9, "sheep"), Enemy(graphics.meanGreen0, 0.7, "greenie"), Enemy(graphics.purplePerp0, 0.5, "purpur")]
outside2.lvrange = [1, 2]

current_map = honeyhome
classvar.player.teleport(current_map.startpoint[0], current_map.startpoint[1])

def new_scale_offset():
    global current_map
    mapw = current_map.finalimage.get_width()
    maph = current_map.finalimage.get_height()
    if mapw<maph:
        smaller = mapw
    else:
        smaller = maph
    if mapw<variables.width or maph<variables.height:
        variables.scaleoffset = variables.width/smaller
    else:
        variables.scaleoffset = 1
    current_map.scale_by_offset()
    classvar.player.scale_by_offset()

def change_map(name):
    global current_map
    if name == "honeyhome":
        current_map = honeyhome
    if name == 'outside1':
        current_map = outside1
    if name == "outside2":
        current_map = outside2
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