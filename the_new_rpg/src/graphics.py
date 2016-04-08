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

bush = pygame.image.load(os.path.join('pics', "bushbkgrdSILR_0.png"))
bush = sscale(bush)

creepcat0 = pygame.image.load(os.path.join('pics', "creepCatSILR_0.png"))
creepcat0 = sscale(creepcat0)

creepcat1 = pygame.image.load(os.path.join('pics', "creepCatSILR_1.png"))
creepcat1 = sscale(creepcat1)

creepcat2 = pygame.image.load(os.path.join('pics', "creepCatSILR_2.png"))
creepcat2 = sscale(creepcat2)

creepcat3 = pygame.image.load(os.path.join('pics', "creepCatSILR_3.png"))
creepcat3 = sscale(creepcat3)

dancelion0 = pygame.image.load(os.path.join('pics', "DanceLionSILR_0.png"))
dancelion0 = sscale(dancelion0)

dancelion1 = pygame.image.load(os.path.join('pics', "DanceLionSILR_1.png"))
dancelion1 = sscale(dancelion1)

evilblob0 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_00.png"))
evilblob0 = sscale(evilblob0)

evilblob1 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_01.png"))
evilblob1 = sscale(evilblob1)

evilblob2 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_02.png"))
evilblob2 = sscale(evilblob2)

evilblob3 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_03.png"))
evilblob3 = sscale(evilblob3)

evilblob4 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_04.png"))
evilblob4 = sscale(evilblob4)

evilblob5 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_05.png"))
evilblob5 = sscale(evilblob5)

evilblob6 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_06.png"))
evilblob6 = sscale(evilblob6)

evilblob7 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_07.png"))
evilblob7 = sscale(evilblob7)

evilblob8 = pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_08.png"))
evilblob8 = sscale(evilblob8)

evilblob9 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_09.png")))

evilblob10 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_10.png")))

evilblob11 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_11.png")))

evilblob12 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_12.png")))

evilblob13 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_13.png")))

evilblob14 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_14.png")))

evilblob15 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_15.png")))

evilblob16 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_16.png")))

evilblob17 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_17.png")))

evilblob18 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_18.png")))

evilblob19 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_19.png")))

evilblob20 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_20.png")))

evilblob21 = sscale(pygame.image.load(os.path.join('pics', "EvilBlobLastFightSILR_21.png")))

warddrobe = sscale(pygame.image.load(os.path.join('pics', "wardrobe.png")))

warddrobe2 = sscale(pygame.image.load(os.path.join('pics', "wardrobe v2.png")))

tree1 = sscale(pygame.image.load(os.path.join('pics', "TreebobSILR_0.png")))

tree2 = sscale(pygame.image.load(os.path.join('pics', "treeSILR_0.png")))

tree3 = sscale(pygame.image.load(os.path.join('pics', "SophiaTree_0")))