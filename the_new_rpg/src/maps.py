#!/usr/bin/python
import pygame, variables, graphics
from Map import Map
from Rock import Rock

block = graphics.test_rock.get_width()
testmap1 = Map(graphics.testmapimage, [Rock(graphics.test_rock, 2*block, 2*block),
                                       Rock(graphics.test_rock, 3*block, 2*block)])