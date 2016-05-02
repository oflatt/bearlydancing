#!/usr/bin/python

import pygame, os, variables

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

#sscale means smart scale, Oliver works on this
#this one does not preserve the original pixel size
def sscale_customfactor(img, factor):
    factor = factor * 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)])

#use if you want pictures where the smaller dimension is a set size
def scale_pure(img, s):
    w = img.get_width()
    h = img.get_height()
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller) * s), int((h/smaller) * s)])

def importpic(filename):
    return pygame.image.load(os.path.join('pics', filename)).convert_alpha()
def simport(filename):
    return sscale(importpic(filename))

testmapimage = importpic('testmap.jpg')
testmapimage = sscale_customfactor(testmapimage, 2)#do not use custom factor on normal art, preserve pixil sizes

#Art by Jacob and Spirit imported
map_base = simport("a path.png")
tree1 = simport("Tree1.png")
tree2 = simport("Tree2.png")
tree3 = simport("Tree3.png")
house = simport("HouseSILR.png")

houseInside = simport("BearHome.png")
#Inside of Bear House
#Bed
bed = simport("Bed JV.png")
#Bed
#Bush
bush = simport("bushbkgrdSILR_0.png")
#Bush
#CowBoy
cowBoy0 = simport('cowboySILR_0.png')

cowBoy1 = simport('cowboySILR_1.png')
#CowBoy
#CreepCat
creepcat0 = simport("creepCatSILR_0.png")

creepcat1 = simport("creepCatSILR_1.png")

creepcat2 = simport("creepCatSILR_2.png")

creepcat3 = simport("creepCatSILR_3.png")
#CreepCat
#DanceLion
dancelion0 = simport("DanceLionSILR_0.png")

dancelion1 = simport("DanceLionSILR_1.png")
#DanceLion
#EvilBlob
evilblob0 = simport("EvilBlobLastFightSILR_00.png")

evilblob1 = simport("EvilBlobLastFightSILR_01.png")

evilblob2 = simport("EvilBlobLastFightSILR_02.png")

evilblob3 = simport("EvilBlobLastFightSILR_03.png")

evilblob4 = simport("EvilBlobLastFightSILR_04.png")

evilblob5 = simport("EvilBlobLastFightSILR_05.png")

evilblob6 = simport("EvilBlobLastFightSILR_06.png")

evilblob7 = simport("EvilBlobLastFightSILR_07.png")

evilblob8 = simport("EvilBlobLastFightSILR_08.png")

evilblob9 = simport("EvilBlobLastFightSILR_09.png")

evilblob10 = simport("EvilBlobLastFightSILR_10.png")

evilblob11 = simport("EvilBlobLastFightSILR_11.png")

evilblob12 = simport("EvilBlobLastFightSILR_12.png")

evilblob13 = simport("EvilBlobLastFightSILR_13.png")

evilblob14 = simport("EvilBlobLastFightSILR_14.png")

evilblob15 = simport("EvilBlobLastFightSILR_15.png")

evilblob16 = simport("EvilBlobLastFightSILR_16.png")

evilblob17 = simport("EvilBlobLastFightSILR_17.png")

evilblob18 = simport("EvilBlobLastFightSILR_18.png")

evilblob19 = simport("EvilBlobLastFightSILR_19.png")

evilblob20 = simport("EvilBlobLastFightSILR_20.png")

evilblob21 = simport("EvilBlobLastFightSILR_21.png")
#EvilBlob
#FMonkey
fmonkey_green = simport("FMonkeyJV0.png")

fmonkey_yellow = simport("FMonkeyJV1.png")

fmonkey_orange = simport("FMonkeyJV2.png")

fmonkey_red = simport("FMonkeyJV3.png")
#FMonkey
#Honey
back_honey0 = simport('HoneyBackSILR_0.png')

back_honey1 = simport('HoneyBackSILR_1.png')

back_honey2 = simport('HoneyBackSILR_2.png')

back_honey3 = simport('HoneyBackSILR_3.png')

front_honey0 = simport('HoneyFrontSILR_0.png')

front_honey1 = simport('HoneyFrontSILR_1.png')

front_honey2 = simport('HoneyFrontSILR_2.png')

front_honey3 = simport('HoneyFrontSILR_3.png')
#this is left
front_honey = simport('honeyLeftSILR_0.png')
#this is left
left_honey1 = simport('honeyLeftSILR_1.png')

left_honey2 = simport('honeyLeftSILR_2.png')

left_honey3 = simport('honeyLeftSILR_3.png')

honey_right0 = simport('HoneyRightSILR_0.png')

honey_right1 = simport('HoneyRightSILR_1.png')

honey_right2 = simport('HoneyRightSILR_2.png')

honey_right3 = simport('HoneyRightSILR_3.png')
#Honey
#Horizontal Map
scrub1 = simport('horizontal.png')
#Horizontal Map
#Jumpy
jumpy1 = simport('JumpySILR_0.png')

jumpy2 = simport('JumpySILR_1.png')
#Jumpy
#Left Turn Map
leftTurn = simport('leftTurn.png')
#Left Turn Map
#Mean Green
meanGreen0 = simport('MeanGreenSILR_0.png')

meanGreen1 =simport('MeanGreenSILR_1.png')
#MeanGreen
#Nice Dog
niceDog0 = simport('NiceDogSILR_0.png')

niceDog1 = simport('NiceDogSILR_1.png')

niceDog2 = simport('NiceDogSILR_2.png')

niceDog3 = simport('NiceDogSILR_3.png')
#NiceDog
#PinkFreak
pinkFreak0 = simport('PinkFreakSILR_00.png')

pinkFreak1 = simport('PinkFreakSILR_01.png')

pinkFreak2 = simport('PinkFreakSILR_02.png')

pinkFreak3 = simport('PinkFreakSILR_03.png')

pinkFreak4 = simport('PinkFreakSILR_04.png')

pinkFreak5 = simport('PinkFreakSILR_05.png')

pinkFreak6 = simport('PinkFreakSILR_06.png')

pinkFreak7 = simport('PinkFreakSILR_07.png')

pinkFreak8 = simport('PinkFreakSILR_08.png')

pinkFreak9 = simport('PinkFreakSILR_09.png')

pinkFreak10 = simport('PinkFreakSILR_10.png')
#PinkFreak
#PurplePerp
purplePerp0 = simport('PurpleperpSILR_0.png')

purplePerp1 = simport('PurpleperpSILR_1.png')

purplePerp2 = simport('PurpleperpSILR_2.png')

purplePerp3 = simport('PurpleperpSILR_3.png')
#PurplePerp
#Queen Bird
queenBird0 = simport('QueenBirdSILR_0.png')
#Queen Bird
#Quiche
quiche0 = simport('QuicheSILR_0.png')
#Quiche
#Trash Panda
tpanda_worried = simport("racoon sad.png")

tpanda =simport("racoon.png")
#Trash Panda
#Right Turn Map
rightTurn = simport('rightTurn.png')
#Right Turn Map
#Rock
rock = simport("Rock JV.png")
#Rock
#Ruderoo
ruderoo0 = simport('ruderooSILR_00.png')

ruderoo1 = simport('ruderooSILR_01.png')

ruderoo2 = simport('ruderooSILR_02.png')

ruderoo3 = simport('ruderooSILR_03.png')

ruderoo4 = simport('ruderooSILR_04.png')

ruderoo5 = simport('ruderooSILR_05.png')

ruderoo6 = simport('ruderooSILR_06.png')

ruderoo7 = simport('ruderooSILR_07.png')

ruderoo8 = simport('ruderooSILR_08.png')

ruderoo9 =simport('ruderooSILR_09.png')

ruderoo10 = simport('ruderooSILR_10.png')
#Ruderoo
#Most important Mob in the game
mostImportantMob0 = simport('ScaryStevenSILR_0.png')

mostImportantMob1 = simport('ScaryStevenSILR_1.png')

mostImportantMob2 = simport('ScaryStevenSILR_2.png')

mostImportantMob3 = simport('ScaryStevenSILR_3.png')
#Most important mob in the game
#Sheep
sheep1 = simport('Sheep1stfightSILR_0.png')

sheep2 = simport('Sheep1stfightSILR_1.png')
#Sheep

#Vertical map
scrub2 = simport('vertical.png')
#Vertical map
#Wardrobe
warddrobe = simport("wardrobe.png")

warddrobe2 = simport("wardrobe v2.png")
#Wardrobe
#Welcome Mat
welcomeMat = simport('welcomematt.png')
#Tall Tree
tall_Tree = simport('tallTree_0.png')
#Tall Tree 2
tall_Tree2 = simport('Bigtree.png')
#Wii_U
wiiu = simport('wiiu.png')
#bush
bush = simport('bush.png')
#tv
tv = simport('tv0.png')
