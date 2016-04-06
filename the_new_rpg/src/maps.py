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

path1 = Map(graphics.map_base, [Rock(graphics.rock, 2*block, 2*block, True),
                                Rock(graphics.bed, 5*block, 4*block, True),
                                Rock(graphics.warddrobe, 10*block, 10*block, True),
                                Rock(graphics.warddrobe2, 3*block, 3*block, True)])

current_map = path1