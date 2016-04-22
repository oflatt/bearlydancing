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
houserock.h = houserock.h * 3/5

# outside 1
outside1 = Map(graphics.scrub1, [
                                Rock(graphics.tree3, 1.4*block, 2.3*block, True),
                                Rock(graphics.tree3, 1.9*block, 2.3*block, True),
                                Rock(graphics.tree3, 2.4*block, 2.3*block, True),
                                Rock(graphics.house, 0*block, 0*block, True),
                                Rock(graphics.tall_Tree, 6*block, 6*block, True)])

outsidewidth = graphics.scrub1.get_width()
outsideheight = graphics.scrub1.get_height()
outside1.startpoint= [block*8,block*4]
outside1.exitareas = [Exit([outsidewidth, 0, 100, outsideheight], False, 'outside2', 0, block*4)]
#outside1.enemies = [Enemy(graphics.sheep1, 0.9, "sheep"), Enemy(graphics.meanGreen0, 1.0, "greenie")]
#outside1.lvrange = [1, 2]
#outside1.conversations = [conversations.testconversation]

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
                                       Rock(graphics.tpanda, 8*insideb, 7*insideb, False)])

honeyhome.startpoint = [0,0]
honeyhome.exitareas = [Exit([insidewidth/2-graphics.welcomeMat.get_width()/2, insideheight,
                             graphics.welcomeMat.get_width(), insideb], False, 'outside1', insideb*0.85, insideb*6)]
racoonc = conversations.firstscene
racoonc.area = [0, 7*insideb, insidewidth, 50]#50 because it does not matter how thick it is down
racoonc.isbutton = False
racoonc.part_of_story = 1 #makes it so you can only have the conversation once
honeyhome.conversations = [racoonc]

outside2 = Map(graphics.leftTurn, [Rock(graphics.bed, 2*block, 4*block, False)])

current_map = outside1
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
    classvar.player.change_of_state()
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