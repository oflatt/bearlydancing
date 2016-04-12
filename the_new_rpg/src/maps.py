#!/usr/bin/python
import pygame, variables, graphics
from Map import Map
from Rock import Rock

block = graphics.front_honey.get_width()
testmap1 = Map(graphics.testmapimage, [Rock(graphics.bed, 2*block, 2*block, True),
                                       Rock(graphics.bed, 3*block, 2*block, True),
                                       Rock(graphics.front_honey, 6*block, 2*block, False)])

testmap1.startpoint = [block * 10, block*10]
testmap1.endarea = [block * 50, block * 50, block * 55, block*55]

#Rock(graphics.(whatever picture), x value, y value, Collision Detection)
path1 = Map(graphics.houseInside, [Rock(graphics.welcomeMat, 2.25*block, 5.1*block, True),
                                   Rock(graphics.bed, 0*block, 0*block, False),
                                   Rock(graphics.warddrobe2, 2*block, 0*block, False),
                                   Rock(graphics.tpanda, 4*block, 4*block, True)])

current_map = path1