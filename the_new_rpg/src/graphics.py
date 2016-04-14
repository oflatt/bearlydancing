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
#path
map_base = pygame.image.load(os.path.join('pics', "a path.png"))
map_base = sscale(map_base)
#path
#Inside of Bear House
houseInside = sscale(pygame.image.load(os.path.join('pics', "BearHome.png")))
#Inside of Bear House
#Bed
bed = pygame.image.load(os.path.join('pics', "Bed JV.png"))
bed = sscale(bed)
#Bed
#Bush
bush = pygame.image.load(os.path.join('pics', "bushbkgrdSILR_0.png"))
bush = sscale(bush)
#Bush
#CowBoy
cowBoy0 = pygame.image.load(os.path.join('pics', 'cowboySILR_0.png'))

cowBoy1 = pygame.image.load(os.path.join('pics', 'cowboySILR_1.png'))
#CowBoy
#CreepCat
creepcat0 = pygame.image.load(os.path.join('pics', "creepCatSILR_0.png"))
creepcat0 = sscale(creepcat0)

creepcat1 = pygame.image.load(os.path.join('pics', "creepCatSILR_1.png"))
creepcat1 = sscale(creepcat1)

creepcat2 = pygame.image.load(os.path.join('pics', "creepCatSILR_2.png"))
creepcat2 = sscale(creepcat2)

creepcat3 = pygame.image.load(os.path.join('pics', "creepCatSILR_3.png"))
creepcat3 = sscale(creepcat3)
#CreepCat
#DanceLion
dancelion0 = pygame.image.load(os.path.join('pics', "DanceLionSILR_0.png"))
dancelion0 = sscale(dancelion0)

dancelion1 = pygame.image.load(os.path.join('pics', "DanceLionSILR_1.png"))
dancelion1 = sscale(dancelion1)
#DanceLion
#EvilBlob
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
#EvilBlob
#FMonkey
fmonkey_green = pygame.image.load(os.path.join('pics', "FMonkeyJV0.png"))
fmonkey_green = sscale(fmonkey_green)

fmonkey_yellow = pygame.image.load(os.path.join('pics', "FMonkeyJV1.png"))
fmonkey_yellow = sscale(fmonkey_yellow)

fmonkey_orange = pygame.image.load(os.path.join('pics', "FMonkeyJV2.png"))
fmonkey_orange = sscale(fmonkey_orange)

fmonkey_red = pygame.image.load(os.path.join('pics', "FMonkeyJV3.png"))
fmonkey_red = sscale(fmonkey_red)
#FMonkey
#Honey
back_honey0 = sscale(pygame.image.load(os.path.join('pics','HoneyBackSILR_0.png')))

back_honey1 = sscale(pygame.image.load(os.path.join('pics','HoneyBackSILR_1.png')))

back_honey2 = sscale(pygame.image.load(os.path.join('pics','HoneyBackSILR_2.png')))

back_honey3 = sscale(pygame.image.load(os.path.join('pics','HoneyBackSILR_3.png')))

front_honey0 = sscale(pygame.image.load(os.path.join('pics','HoneyFrontSILR_0.png')))

front_honey1 = sscale(pygame.image.load(os.path.join('pics','HoneyFrontSILR_1.png')))

front_honey2 = sscale(pygame.image.load(os.path.join('pics','HoneyFrontSILR_2.png')))

front_honey3 = sscale(pygame.image.load(os.path.join('pics','HoneyFrontSILR_3.png')))

left_honey0 = sscale(pygame.image.load(os.path.join('pics','honeyLeftSILR_0.png')))

left_honey1 = sscale(pygame.image.load(os.path.join('pics','honeyLeftSILR_1.png')))

left_honey2 = sscale(pygame.image.load(os.path.join('pics','honeyLeftSILR_2.png')))

left_honey3 = sscale(pygame.image.load(os.path.join('pics','honeyLeftSILR_3.png')))

honeyRight0 = sscale(pygame.image.load(os.path.join('pics','HoneyRightSILR_0.png')))

honeyRight1 = sscale(pygame.image.load(os.path.join('pics','HoneyRightSILR_1.png')))

honeyRight2 = sscale(pygame.image.load(os.path.join('pics','HoneyRightSILR_2.png')))

honeyRight3 = sscale(pygame.image.load(os.path.join('pics','HoneyRightSILR_3.png')))
#Honey
#Horizontal Map
scrub1 = sscale(pygame.image.load(os.path.join('pics','horizontal.png')))
#Horizontal Map
#House Sprite
house = sscale(pygame.image.load(os.path.join('pics', "HouseSILR.png")))
#House Sprite
#Jumpy
jumpy1 = sscale(pygame.image.load(os.path.join('pics','JumpySILR_0.png')))

jumpy2 = sscale(pygame.image.load(os.path.join('pics', 'JumpySILR_1.png')))
#Jumpy
#Left Turn Map
leftTurn = sscale(pygame.image.load(os.path.join('pics', 'leftTurn.png')))
#Left Turn Map
#Mean Green
meanGreen0 = sscale(pygame.image.load(os.path.join('pics', 'MeanGreenSILR_0.png')))

meanGreen1 = sscale(pygame.image.load(os.path.join('pics','MeanGreenSILR_1.png')))
#MeanGreen
#Nice Dog
niceDog0 = sscale(pygame.image.load(os.path.join('pics','NiceDogSILR_0.png')))

niceDog1 = sscale(pygame.image.load(os.path.join('pics','NiceDogSILR_1.png')))

niceDog2 = sscale(pygame.image.load(os.path.join('pics','NiceDogSILR_2.png')))

niceDog3 = sscale(pygame.image.load(os.path.join('pics','NiceDogSILR_3.png')))
#NiceDog
#PinkFreak
pinkFreak0 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_00.png')))

pinkFreak1 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_01.png')))

pinkFreak2 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_02.png')))

pinkFreak3 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_03.png')))

pinkFreak4 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_04.png')))

pinkFreak5 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_05.png')))

pinkFreak6 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_06.png')))

pinkFreak7 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_07.png')))

pinkFreak8 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_08.png')))

pinkFreak9 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_09.png')))

pinkFreak10 = sscale(pygame.image.load(os.path.join('pics','PinkFreakSILR_10.png')))
#PinkFreak
#PurplePerp
purplePerp0 = sscale(pygame.image.load(os.path.join('pics','PurpleperpSILR_0.png')))

purplePerp1 = sscale(pygame.image.load(os.path.join('pics','PurpleperpSILR_1.png')))

purplePerp2 = sscale(pygame.image.load(os.path.join('pics','PurpleperpSILR_2.png')))

purplePerp3 = sscale(pygame.image.load(os.path.join('pics','PurpleperpSILR_3.png')))
#PurplePerp
#Queen Bird
queenBird0 = sscale(pygame.image.load(os.path.join('pics','QueenBirdSILR_0.png')))
#Queen Bird
#Quiche
quiche0 = sscale(pygame.image.load(os.path.join('pics','QuicheSILR_0.png')))
#Quiche
#Trash Panda
tpanda_worried = pygame.image.load(os.path.join('pics', "racoon sad.png"))

tpanda = pygame.image.load(os.path.join('pics', "racoon.png"))
#Trash Panda
#Right Turn Map
rightTurn = pygame.image.load(os.path.join('pics','rightTurn.png'))
#Right Turn Map
#Rock
rock = pygame.image.load(os.path.join('pics', "Rock JV.png"))
rock = sscale(rock)
#Rock
#Ruderoo
ruderoo0 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_00.png')))

ruderoo1 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_01.png')))

ruderoo2 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_02.png')))

ruderoo3 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_03.png')))

ruderoo4 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_04.png')))

ruderoo5 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_05.png')))

ruderoo6 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_06.png')))

ruderoo7 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_07.png')))

ruderoo8 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_08.png')))

ruderoo9 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_09.png')))

ruderoo10 = sscale(pygame.image.load(os.path.join('pics','ruderooSILR_10.png')))
#Ruderoo
#Most important Mob in the game
mostImportantMob0 = sscale(pygame.image.load(os.path.join('pics','ScaryStevenSILR_0.png')))

mostImportantMob1 = sscale(pygame.image.load(os.path.join('pics','ScaryStevenSILR_1.png')))

mostImportantMob2 = sscale(pygame.image.load(os.path.join('pics', 'ScaryStevenSILR_2.png')))

mostImportantMob3 = sscale(pygame.image.load(os.path.join('pics','ScaryStevenSILR_3.png')))
#Most important mob in the game
#Sheep
sheep1 = sscale(pygame.image.load(os.path.join('pics', 'Sheep1stfightSILR_0.png')))

sheep2 = sscale(pygame.image.load(os.path.join('pics', 'Sheep1stfightSILR_1.png')))
#Sheep
#Trees
tree1 = sscale(pygame.image.load(os.path.join('pics', "Tree1.png")))

tree2 = sscale(pygame.image.load(os.path.join('pics', "Tree2.png")))

tree3 = sscale(pygame.image.load(os.path.join('pics', "Tree3.png")))
#Trees
#Vertical map
scrub2 = sscale(pygame.image.load(os.path.join('pics', 'vertical.png')))
#Vertical map
#Wardrobe
warddrobe = sscale(pygame.image.load(os.path.join('pics', "wardrobe.png")))

warddrobe2 = sscale(pygame.image.load(os.path.join('pics', "wardrobe v2.png")))
#Wardrobe
#Welcome Mat
welcomeMat = sscale(pygame.image.load(os.path.join('pics', 'welcomematt.png')))
#Welcome Mat
