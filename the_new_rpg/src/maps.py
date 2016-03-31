#!/usr/bin/python
import pygame, variables, graphics
from Map import Map
from Rock import Rock

block = graphics.test_rock.get_width()
testmap1 = Map(graphics.testmapimage, [Rock(graphics.test_rock, 2*block, 2*block),
                                       Rock(graphics.test_rock, 3*block, 2*block),
                                       Rock(graphics.front_honey, 6*block, 2*block)])

testmap1.startpoint = [block * 10, block*10]
testmap1.endarea = [block * 50, block * 50, block * 55, block*55]