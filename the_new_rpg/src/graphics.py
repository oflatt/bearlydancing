#!/usr/bin/python

import pygame, os, variables

#sscale means smart scale, Oliver works on this
#factor cannot be less than one, because that would make it smaller than the window
def sscale(img, factor):
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize), int((h/smaller)*endsize)])

#Oliver's example- make sure to put .convert() at the end to make it run faster (as a png)
testmapimage = pygame.image.load(os.path.join('testmap.jpg')).convert()
testmapimage = sscale(testmapimage, 3)