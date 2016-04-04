#!/usr/bin/python

import pygame, os, variables

#sscale means smart scale, Oliver works on this
#this one does not preserve the original pixel size
def sscale_customfactor(img, factor):
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize), int((h/smaller)*endsize)])

def sscale(img):
    factor = 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)])

#Oliver's example- make sure to put .convert() at the end to make it run faster (as a png)
testmapimage = pygame.image.load(os.path.join('pics', 'testmap.jpg'))
testmapimage = sscale_customfactor(testmapimage, 2)#do not use custom factor without reason-preserve pixil sizes

#example code of loading an image
#test_rock = pygame.image.load(os.path.join('pics', 'pokemon_grass.png'))
#test_rock = sscale(test_rock)

#Art by Jacob and Spirit imported
front_honey = pygame.image.load(os.path.join('pics', "honeySILR_0.png"))
front_honey = sscale(front_honey)

honey_right1 = pygame.image.load(os.path.join('pics', "HoneyRightSILR_0.png"))
honey_right1 = sscale(honey_right1)

bed = pygame.image.load(os.path.join('pics', "Bed JV.png"))
bed = sscale(bed)

rock = pygame.image.load(os.path.join('pics', "Rock JV.png"))
rock = sscale(rock)

tpanda = pygame.image.load(os.path.join('pics', "Trash Panda aka T.P JV.png"))
tpanda = sscale(tpanda)

tpanda_worried = pygame.image.load(os.path.join('pics', "Trash Panda aka T.P worried face JV.png"))
tpanda_worried= sscale(tpanda_worried)

fmonkey_green = pygame.image.load(os.path.join('pics', "FMonkeyJV0.png"))
fmonkey_green = sscale(fmonkey_green)

fmonkey_yellow = pygame.image.load(os.path.join('pics', "FMonkeyJV1.png"))
fmonkey_yellow = sscale(fmonkey_yellow)

fmonkey_orange = pygame.image.load(os.path.join('pics', "FMonkeyJV2.png"))
fmonkey_orange = sscale(fmonkey_orange)

fmonkey_red = pygame.image.load(os.path.join('pics', "FMonkeyJV3.png"))
fmonkey_red = sscale(fmonkey_red)

map_base = pygame.image.load(os.path.join('pics', "a path.png"))
map_base = sscale(map_base)
