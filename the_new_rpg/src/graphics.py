#!/usr/bin/python

import pygame, os, variables

#sscale means smart scale, Oliver works on this
def sscale(img, factor):
    ...

#Oliver's example- make sure to put .convert() at the end to make it run faster (as a png)
testmapimage = pygame.image.load(os.path.join('testmap.jpg')).convert()