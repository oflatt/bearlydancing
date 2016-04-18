#!/usr/bin/python
import pygame, variables, graphics, classvar, conversations
from Map import Map
from Rock import Rock
from Exit import Exit
from Enemy import Enemy

block = variables.width/10
testmap1 = Map(graphics.testmapimage, [Rock(graphics.bed, 2*block, 2*block, True),
                                       Rock(graphics.bed, 3*block, 2*block, True),
                                       Rock(graphics.front_honey, 6*block, 2*block, False)])
testmap1.startpoint = [block * 10, block*10]

#Rock(graphics.(whatever picture), x value, y value, Collision Detection)
house1 = Map(graphics.houseInside, [Rock(graphics.welcomeMat, 2.25*block, 5.3*block, False),
                                   Rock(graphics.bed, 0*block, 0*block, False),
                                   Rock(graphics.warddrobe2, 2*block, 0*block, False),
                                   Rock(graphics.tpanda, 4*block, 5*block, True)])
#blank.endpoint (top left x, top left y, bottom right x, bottom right y)
house1.startpoint = [0,0]
house1.endpoint = [block*2,block*4,block*2.5,block*5.5]


houserock = Rock(graphics.house, 0, 0, True)
houserock.h = houserock.h * 3/5

# outside 1
outside1 = Map(graphics.scrub1, [houserock,
                                Rock(graphics.welcomeMat, 0.4*block,3*block, False),
                                Rock(graphics.tree1, 5*block, 3*block, True),
                                Rock(graphics.tree1, 2.1*block, 3*block, True),
                                Rock(graphics.tree3, 2.2*block, 3*block, True),
                                Rock(graphics.tree3, 2.5*block, 3.2*block, True)])

outside1.startpoint = [block *0.85, block*2.9]
outside1.exitareas = [Exit([block*6, block*6, block, block], True, 'outside1', block *0.85, block*2.9)]
outside1.enemies = [Enemy(graphics.sheep1, 0.9, "sheep"), Enemy(graphics.meanGreen0, 1.0, "greenie")]
outside1.lvrange = [1, 2]
conversations.testconversation.area = [block*4, block*4, block, block*2]
outside1.conversations = [conversations.testconversation]

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
    global current_map
    if name == "house1":
        current_map = house1
    if name == 'outside1':
        current_map = outside1
    new_scale_offset()

def on_key(key):
    if key in variables.enterkeys:
        e = current_map.checkexit()
        c = current_map.checkconversation()
        if not e == False:
            classvar.player.teleport(e.newx, e.newy)
            change_map(e.name)
        elif not c == False:
            variables.state = "conversation"
            conversations.currentconversation = c

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
            variables.state = "conversation"
            conversations.currentconversation = c