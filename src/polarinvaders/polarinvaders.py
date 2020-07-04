import pygame, math, random, sys, os, gc
from typing import Dict

import variables
from .spriteSheetToList import *
from graphics import getTextPic
from Game import Game
from .PolarGame import PolarGame


rotatecache : Dict[str, pygame.Surface] = {}
def rotateandcache(name, pic, degrees):
    name = name + str(int(degrees))
    if not name in rotatecache:
        rotatecache[name] = pygame.transform.rotate(pic, int(degrees))
        
    return rotatecache[name]
        

gamename = "polarinvaders"
polargame = None

class Enemy:

    def __init__(self, health, dAngle, dRadius, angle, radius, change, firingRate, image, bulletImage):
        self.h = health
        self.dTh = dAngle
        self.dR = dRadius
        self.th = angle
        self.r = radius
        self.totalH = health
        self.pos = [self.r*math.cos(self.th)+polargame.cen[0], self.r*math.sin(self.th)+polargame.cen[1]]
        self.img = image
        self.mask = pygame.mask.from_surface(image)
        self.dead = False
        self.bImg = bulletImage
        self.ch = change.copy()
        #changeBoolean
        self.chB = False
        #bulletSpeed
        self.bS = 3
        #firingRate
        self.fR = int(10*math.sqrt(random.randint(int(firingRate[0]),int(firingRate[1]))))
        #firingCount
        self.fC = random.randint(0,int(self.fR-1))

    def update(self):
        self.firing()
        self.movement()
        self.collision()

    def firing(self):
        self.fC+=1
        if self.fC >= self.fR:
            self.fC = 0
            polargame.eBullets.append(EBullet([self.pos[0]+24*math.cos(self.th), self.pos[1]+24*math.sin(self.th)], self.th+math.pi, self.bS, self.bImg))

    def movement(self):
        timefactor = polargame.dTime/(1000.0/60)
        if self.ch[0] > 0 and self.r >= self.ch[0] and not self.chB:
            self.dR-=self.ch[1]
            self.dTh-=self.ch[2]
            self.chB = True
        self.th+=self.dTh*timefactor
        self.r+=self.dR*timefactor
        self.pos = [self.r*math.cos(self.th)+polargame.cen[0], self.r*math.sin(self.th)+polargame.cen[1]]

    def display(self, screen):
        self.currentIm = self.img
        self.currentIm = rotateandcache("enemy", self.currentIm, 180*(3*math.pi/2-self.th)/math.pi)
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > polargame.width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > polargame.width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if self.h <= 0:
            self.dead = True
        if not self.dead:
            if self.mask.overlap(pMask, (int(polargame.pos[0]-polargame.pSize/2)-int(self.pos[0]-self.currentImRect.width/2), int(polargame.pos[1]-polargame.pSize/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                polargame.pHealth-=1
                self.dead = True
        
class EBullet:

    def __init__(self, position, angle, speed, image):
        self.pos = position.copy()
        self.th = angle
        self.sp = speed
        self.img = image
        self.dead = False
        self.mask = pygame.mask.from_surface

    def update(self):
        self.movement()
        self.collision()

    def movement(self):
        self.pos[0]+=math.cos(math.pi+self.th)*self.sp
        self.pos[1]+=math.sin(math.pi+self.th)*self.sp
    
    def display(self, screen):
        self.currentIm = self.img
        self.currentIm = rotateandcache("bullet", self.currentIm, 180*(math.pi/2-self.th)/math.pi)
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > polargame.width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > polargame.width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if not self.dead:
            if self.mask.overlap(pMask, (int(polargame.pos[0]-polargame.currentImRect.width/2)-int(self.pos[0]-self.currentImRect.width/2), int(polargame.pos[1]-polargame.currentImRect.height/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                polargame.pHealth-=1
                self.dead = True


class PBullet:

    def __init__(self, position, angle, speed, image):
        self.pos = position.copy()
        self.th = angle
        self.sp = speed
        self.img = image
        self.dead = False
        self.mask = pygame.mask.from_surface(image)
        self.currentIm = self.img
        self.currentIm = rotateandcache("pbullet", self.currentIm, 180*(math.pi/2-self.th)/math.pi)

    def update(self):
        self.movement()
        self.collision()

    def movement(self):
        timefactor =  polargame.dTime/(1000.0/60)
        self.pos[0]+=math.cos(math.pi+self.th)*self.sp*timefactor
        self.pos[1]+=math.sin(math.pi+self.th)*self.sp*timefactor
    
    def display(self, screen):
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > polargame.width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > polargame.width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if not self.dead:
            for enemy in polargame.enemies:
                if self.mask.overlap(enemy.mask, (int(enemy.pos[0]-enemy.currentImRect.width/2)-int(self.pos[0]-self.currentImRect.width/2), int(enemy.pos[1]-enemy.currentImRect.height/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                    enemy.h-=1
                    self.dead = True
def remove():
    rB = 0
    while rB < len(polargame.pBullets):
        if polargame.pBullets[rB].dead:
            del polargame.pBullets[rB]
            rB-=1
        rB+=1
    rB = 0
    while rB < len(polargame.eBullets):
        if polargame.eBullets[rB].dead:
            del polargame.eBullets[rB]
            rB-=1
        rB+=1
    rB = 0
    while rB < len(polargame.enemies):
        if polargame.enemies[rB].dead:
            polargame.score+=100*polargame.enemies[rB].totalH
            del polargame.enemies[rB]
            rB-=1
        rB+=1


def drawboostimg(screen, boostimage, boostimgname):
    currentIm = rotateandcache(boostimgname, boostimage, 180*(math.pi/2-polargame.theta)/math.pi)
    polargame.currentImRect = currentIm.get_rect()
    screen.blit(currentIm, (polargame.pos[0]-polargame.currentImRect.width/2, polargame.pos[1] - polargame.currentImRect.height/2))


def drawmenu(time, settings, screen):
    title = getTextPic("polar invaders", screen.get_height()/8, color = (255,255,255))
    titlerect = title.get_rect()
    titlerect.center = (screen.get_width()/2, 0)
    titlerect.top = screen.get_height()/5

    score = getTextPic("high score: : "+ str(settings.getgamedata(gamename)), screen.get_height()/12, color = (255, 255, 255))
    scorerect = score.get_rect()
    scorerect.center = (screen.get_width()/2, 0)
    scorerect.top = screen.get_height()/2
    
    screen.blit(title, titlerect)
    screen.blit(score, scorerect)
        
def ondraw(time, settings, screen):

    screen.fill((0,0,0))
    for i in range(len(polargame.starValues)):
        pygame.draw.rect(screen, polargame.starValues[i][0],
                         polargame.starValues[i][1], 0)
    for bullet in polargame.eBullets:
        bullet.display(screen)
    for enemy in polargame.enemies:
        enemy.display(screen)
    for bullet in polargame.pBullets:
        bullet.display(screen)
    
    polargame.count += polargame.animationSpeed*polargame.dTime

    if polargame.mainBoost:
        drawboostimg(screen, mainBooster[int(polargame.count)%4], "main")

    if polargame.rightBoost:
        drawboostimg(screen, rightBooster[int(polargame.count)%4], "right")

    if polargame.leftBoost:
        drawboostimg(screen, leftBooster[int(polargame.count)%4], "left")



    text = getTextPic("score:  " + str(polargame.score) + "   health:  " + str(polargame.pHealth), int(variables.gettextsize()*0.6), color = (255,min(max(0, polargame.pHealth*255/30), 255),min(max(0, polargame.pHealth*255/30), 255)))
    textrect = text.get_rect()
    textrect.center = (polargame.width/2, 0)
    textrect.top = 0
    screen.blit(text, textrect)
    if polargame.gamestate == "menu":
        drawmenu(time, settings, screen)

    variables.dirtyupdateall()

    

def movement():
    
    if not polargame.mainBoost:
        if polargame.leftBoost and not polargame.rightBoost:
            polargame.dTheta-=polargame.pSpeed*polargame.dTime*6/100
        elif polargame.rightBoost and not polargame.leftBoost:
            polargame.dTheta+=polargame.pSpeed*polargame.dTime*6/100
    polargame.dTheta*=.99
    polargame.theta+=polargame.dTheta
    polargame.pos = [polargame.radius*math.cos(polargame.theta)+polargame.cen[0], polargame.radius*math.sin(polargame.theta)+polargame.cen[1]]

def waves():
    if len(polargame.enemies) == 0 and len(polargame.eBullets) == 0 and polargame.doneWave:
        polargame.newWave = True
        polargame.waveNum = random.randint(0,3)
        polargame.diff+=0
        if polargame.diff%2 == 0:
            polargame.eHealth+=1
    if polargame.newWave:
        polargame.waveCounter = 0
        polargame.newWave = False
        polargame.doneWave = False
    
    

    # rings of ships move out and turn
    if polargame.waveNum == 0:
        if polargame.waveCounter%64 == 0 and polargame.waveCounter<=192:
            for i in range(8):
                polargame.enemies.append(Enemy(polargame.eHealth, math.pi/200, .9, i*math.pi/4, 20, [120, .7, 0], [70-polargame.diff/2,80-polargame.diff/2], enemy, eBullet))
        elif polargame.waveCounter > 192:
            polargame.doneWave = True

    # rings of ships move out
    if polargame.waveNum == 1:
        if polargame.waveCounter%64 == 0 and polargame.waveCounter<=128:
            for i in range(16-4*int(polargame.waveCounter/64)):
                polargame.enemies.append(Enemy(polargame.eHealth, math.pi/120*(1-polargame.waveCounter%128/32), 2, i*2*math.pi/(16-4*int(polargame.waveCounter/64)), 20, [int(175-polargame.waveCounter*50/64), 2, 0], [70-polargame.diff/2,80-polargame.diff/2], enemy, eBullet))
        elif polargame.waveCounter > 128:
            polargame.doneWave = True

    # some ships stay in a line
    if polargame.waveNum == 2:
        if polargame.waveCounter%50 == 0 and polargame.waveCounter<=250:
            for i in range(8):
                polargame.enemies.append(Enemy(polargame.eHealth, 0, 1, i*math.pi/4, 20, [300-polargame.waveCounter, 1, math.pi/400*(2-((polargame.waveCounter%100)/25))/2], [70-polargame.diff/2,70-polargame.diff/2], enemy, eBullet))
        elif polargame.waveCounter > 250:
            polargame.doneWave = True

    # spirol of ships moves out
    if polargame.waveNum == 3:
        if polargame.waveCounter%6 == 0 and polargame.waveCounter<=180:
            polargame.enemies.append(Enemy(polargame.eHealth, math.pi/90, .6, math.pi/2, 20, [200, .6, math.pi/120], [70-polargame.diff/2,70-polargame.diff/2], enemy, eBullet))
        elif polargame.waveCounter > 540:
            polargame.doneWave = True
            
    polargame.waveCounter+=1

###
#variables
###
def getpic(name):
    return pygame.image.load(os.path.join(variables.pathtoself, "polarinvaders/" + name)).convert_alpha()
eBullet = getpic("eBullet.png")
enemy = getpic("enemy.png")
laser = getpic("laser.png")
leftBooster = getpic("leftBooster.png")
mainBooster = getpic("mainBooster.png")
rightBooster = getpic("rightBooster.png") 
leftBooster = spriteSheetToList(leftBooster, 4)
mainBooster = spriteSheetToList(mainBooster, 4)
rightBooster = spriteSheetToList(rightBooster, 4)
pMask = pygame.mask.from_surface(mainBooster[0])



def init(settings, screen):
    
    if settings.getgamedata(gamename) == None:
        settings.setgamedata(gamename, 0)
    
    global polargame
    polargame = PolarGame(settings, screen)

def onkeydown(time, settings, key):
    onkeyupordown(time, settings, key, True)

def onkeyup(time, settings, key):
    onkeyupordown(time, settings, key, False)
    
def onkeyupordown(time, settings, key, keydownp):
    if polargame.gamestate == "play":

        
        if settings.iskey("left", key):
            polargame.rightBoost = keydownp
        elif settings.iskey("right", key):
            polargame.leftBoost = keydownp

        if not polargame.leftBoost and not polargame.rightBoost:
            polargame.mainBoost = True
        else:
            polargame.mainBoost = False


        if settings.iskey("action", key):
            polargame.actionHeld = keydownp


    elif polargame.gamestate == "menu":
        if settings.iskey("action", key):
            if keydownp:
                init(settings, polargame.screen)
                polargame.gamestate = "play"

def handlefiring():

    polargame.firingCount += 1
    
    if polargame.actionHeld and polargame.firingCount >= polargame.firingRate:
        polargame.firingCount = 0
        theAngle1 = polargame.theta+math.atan(-22/13)
        theAngle2 = polargame.theta+math.atan(22/13)
        coeff1 = math.sqrt(400)
        coeff2 = math.sqrt(400)
        polargame.pBullets.append(PBullet([polargame.pos[0]-coeff1*math.cos(theAngle1), polargame.pos[1]-coeff1*math.sin(theAngle1)], polargame.theta, polargame.pBulletSpeed, laser))
        polargame.pBullets.append(PBullet([polargame.pos[0]-coeff1*math.cos(theAngle2), polargame.pos[1]-coeff1*math.sin(theAngle2)], polargame.theta, polargame.pBulletSpeed, laser))
    
    
def ontick(time, settings):
    
    # exit to main menu on death
    if polargame.pHealth <= 0:
        if polargame.score > settings.getgamedata(gamename):
            settings.setgamedata(gamename, polargame.score)
        polargame.gamestate = "menu"
    if polargame.gamestate == "play":
        polargame.dTime = time-polargame.oldtime

        for bullet in polargame.eBullets:
            bullet.update()
        for enemy in polargame.enemies:
            enemy.update()
        for bullet in polargame.pBullets:
            bullet.update()

        handlefiring()
        waves()
        movement()
        remove()
        
    elif polargame.gamestate == "menu":
        pass

    polargame.oldtime = time

def pause(currenttime):
    polargame.leftBoost = False
    polargame.rightBoost = False
    polargame.mainBoost = True


def unpause(currenttime):
    pass

    
def creategame():
    return Game(gamename, init, onkeydown, onkeyup, ontick, ondraw, pause, unpause)
    
    
