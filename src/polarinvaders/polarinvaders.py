import pygame, math, random, sys
from .spriteSheetToList import *

import variables
from graphics import getTextPic
from Game import Game

# stored as global
screen = None

class Enemy:

    def __init__(self, health, dAngle, dRadius, angle, radius, change, firingRate, image, bulletImage):
        self.h = health
        self.dTh = dAngle
        self.dR = dRadius
        self.th = angle
        self.r = radius
        self.totalH = health
        self.pos = [self.r*math.cos(self.th)+cen[0], self.r*math.sin(self.th)+cen[1]]
        self.img = image.copy()
        self.mask = pygame.mask.from_surface(image)
        self.dead = False
        self.bImg = bulletImage.copy()
        self.ch = change.copy()
        #changeBoolean
        self.chB = False
        #bulletSpeed
        self.bS = 3
        #firingRate
        self.fR = random.randint(firingRate[0],firingRate[1])
        #firingCount
        self.fC = random.randint(0,self.fR-1)

    def update(self):
        self.firing()
        self.movement()
        self.display()
        self.collision()

    def firing(self):
        self.fC+=1
        if self.fC >= self.fR:
            self.fC = 0
            eBullets.append(EBullet([self.pos[0]+24*math.cos(self.th), self.pos[1]+24*math.sin(self.th)], self.th+math.pi, self.bS, self.bImg))

    def movement(self):
        if self.ch[0] > 0 and self.r >= self.ch[0] and not self.chB:
            self.dR-=self.ch[1]
            self.dTh-=self.ch[2]
            self.chB = True
        self.th+=self.dTh
        self.r+=self.dR
        self.pos = [self.r*math.cos(self.th)+cen[0], self.r*math.sin(self.th)+cen[1]]

    def display(self):
        self.currentIm = self.img.copy()
        self.currentIm = pygame.transform.rotate(self.currentIm, 180*(3*math.pi/2-self.th)/math.pi)
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if self.h <= 0:
            self.dead = True
        if not self.dead:
            global pHealth
            if self.mask.overlap(pMask, (int(pos[0]-pSize/2)-int(self.pos[0]-self.currentImRect.width/2), int(pos[1]-pSize/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                pHealth-=1
                self.dead = True
        
class EBullet:

    def __init__(self, position, angle, speed, image):
        self.pos = position.copy()
        self.th = angle
        self.sp = speed
        self.img = image.copy()
        self.dead = False
        self.mask = pygame.mask.from_surface

    def update(self):
        self.movement()
        self.collision()

    def movement(self):
        self.pos[0]+=math.cos(math.pi+self.th)*self.sp
        self.pos[1]+=math.sin(math.pi+self.th)*self.sp
    
    def display(self):
        self.currentIm = self.img.copy()
        self.currentIm = pygame.transform.rotate(self.currentIm, 180*(math.pi/2-self.th)/math.pi)
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if not self.dead:
            global currentImRect
            global pHealth
            if self.mask.overlap(pMask, (int(pos[0]-currentImRect.width/2)-int(self.pos[0]-self.currentImRect.width/2), int(pos[1]-currentImRect.height/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                pHealth-=1
                self.dead = True


class PBullet:

    def __init__(self, position, angle, speed, image):
        self.pos = position.copy()
        self.th = angle
        self.sp = speed
        self.img = image
        self.dead = False
        self.mask = pygame.mask.from_surface(image)

    def update(self):
        self.movement()
        self.collision()

    def movement(self):
        self.pos[0]+=math.cos(math.pi+self.th)*self.sp
        self.pos[1]+=math.sin(math.pi+self.th)*self.sp
    
    def display(self):
        self.currentIm = self.img.copy()
        self.currentIm = pygame.transform.rotate(self.currentIm, 180*(math.pi/2-self.th)/math.pi)
        self.currentImRect = self.currentIm.get_rect()
        self.mask = pygame.mask.from_surface(self.currentIm)
        screen.blit(self.currentIm, (self.pos[0]-self.currentImRect.width/2, self.pos[1]-self.currentImRect.height/2))

    def collision(self):
        if self.pos[0] > width or self.currentImRect.width+self.pos[0] < 0:
            self.dead = True
        elif self.pos[1] > width or self.currentImRect.height+self.pos[1] < 0:
            self.dead = True
        if not self.dead:
            for enemy in enemies:
                if self.mask.overlap(enemy.mask, (int(enemy.pos[0]-enemy.currentImRect.width/2)-int(self.pos[0]-self.currentImRect.width/2), int(enemy.pos[1]-enemy.currentImRect.height/2)-int(self.pos[1]-self.currentImRect.height/2))) != None:
                    enemy.h-=1
                    self.dead = True
def remove():
    rB = 0
    while rB < len(pBullets):
        if pBullets[rB].dead:
            pBullets.pop(rB)
            rB-=1
        rB+=1
    rB = 0
    while rB < len(eBullets):
        if eBullets[rB].dead:
            eBullets.pop(rB)
            rB-=1
        rB+=1
    rB = 0
    while rB < len(enemies):
        if enemies[rB].dead:
            global score
            score+=100*enemies[rB].totalH
            enemies.pop(rB)
            rB-=1
        rB+=1


def drawboostimg(screen, boostimage):
    currentIm = pygame.transform.rotate(boostimage, 180*(math.pi/2-theta)/math.pi)
    currentImRect = currentIm.get_rect()
    screen.blit(currentIm, (pos[0]-currentImRect.width/2, pos[1] - currentImRect.height/2))
    
        
def ondraw(time, settings, screenin):
    global screen
    screen = screenin
    
    screen.fill((0,0,0))
    for i in range(len(starValues)):
        pygame.draw.rect(screen, starValues[i][0],
                         starValues[i][1], 0)
    for bullet in eBullets:
        bullet.display()
    for enemy in enemies:
        enemy.display()
    for bullet in pBullets:
        bullet.display()
    global count
    count += animationSpeed*dTime

    if mainBoost:
        drawboostimg(screen, mainBooster[int(count)%4].copy())

    if rightBoost:
        drawboostimg(screen, leftBooster[int(count)%4].copy())
        
    if leftBoost:
        drawboostimg(screen, rightBooster[int(count)%4].copy())
    
    
    text = getTextPic("score:  " + str(score) + "   health:  " + str(pHealth), int(variables.gettextsize()*0.6), color = (255,min(max(0, pHealth*255/30), 255),min(max(0, pHealth*255/30), 255)), savep = False)
    textrect = text.get_rect()
    textrect.center = (width/2, 0)
    textrect.top = 0
    screen.blit(text, textrect)

    

def movement():
    global theta
    global pos
    global dTheta
    if not mainBoost:
        if leftBoost:
            dTheta-=pSpeed*dTime*6/100
        else:
            dTheta+=pSpeed*dTime*6/100
    dTheta*=.99
    theta+=dTheta
    pos = [radius*math.cos(theta)+cen[0], radius*math.sin(theta)+cen[1]]

def waves():
    global doneWave
    global eHealth
    global enemy
    global waveNum
    global newWave
    global waveCounter
    global diff
    if len(enemies) == 0 and len(eBullets) == 0 and doneWave:
        newWave = True
        waveNum = random.randint(0,3)
        diff+=0
        if diff%2 == 0:
            eHealth+=1
    if newWave:
        waveCounter = 0
        newWave = False
        doneWave = False
    if waveNum == 0:
        if waveCounter%64 == 0 and waveCounter<=192:
            for i in range(8):
                enemies.append(Enemy(eHealth, math.pi/200, .9, i*math.pi/4, 20, [120, .7, 0], [70-diff,80-diff], enemy, eBullet))
        elif waveCounter > 192:
            doneWave = True
    if waveNum == 1:
        if waveCounter%64 == 0 and waveCounter<=128:
            for i in range(16-4*int(waveCounter/64)):
                enemies.append(Enemy(eHealth, math.pi/120*(1-waveCounter%128/32), 2, i*2*math.pi/(16-4*int(waveCounter/64)), 20, [int(175-waveCounter*50/64), 2, 0], [70-diff,80-diff], enemy, eBullet))
        elif waveCounter > 128:
            doneWave = True
    if waveNum == 2:
        if waveCounter%50 == 0 and waveCounter<=250:
            for i in range(8):
                enemies.append(Enemy(eHealth, 0, 1, i*math.pi/4, 20, [300-waveCounter, 1, math.pi/400*(2-((waveCounter%100)/25))/2], [70-diff,70-diff], enemy, eBullet))
        elif waveCounter > 250:
            doneWave = True
    if waveNum == 3:
        if waveCounter%24 == 0 and waveCounter<=696:
            enemies.append(Enemy(eHealth, math.pi/90, .6, math.pi/2, 20, [200, .6, math.pi/120-.08], [70-diff,70-diff], enemy, eBullet))
        elif waveCounter > 540:
            doneWave = True
    waveCounter+=1

###
#variables
###
eBullet = pygame.image.load("polarinvaders/eBullet.png")
enemy = pygame.image.load("polarinvaders/enemy.png")
laser = pygame.image.load("polarinvaders/laser.png")
leftBooster = pygame.image.load("polarinvaders/leftBooster.png")
mainBooster = pygame.image.load("polarinvaders/mainBooster.png")
rightBooster = pygame.image.load("polarinvaders/rightBooster.png")
leftBooster = spriteSheetToList(leftBooster, 4)
mainBooster = spriteSheetToList(mainBooster, 4)
rightBooster = spriteSheetToList(rightBooster, 4)
pMask = pygame.mask.from_surface(mainBooster[0])


pBulletSpeed = 7
firingCount = 0
firingRate = 10


def init(screen):
    global cen
    global pos
    global width
    global height
    global score, eBullets, starValues, cen, theta, radius, pos, ringRadius
    global pSize, count, dTheta, pSpeed, animationSpeed, time, dTime, actionHeld
    global mainBoost, leftBoost, rightBoost, pBullets, enemies, pHealth, waveNum
    global newWave, doneWave, waveCounter, eHealth, diff, currentImRect


    score = 0
    eBullets = []
    starValues = []
    cen = None
    theta = math.pi/2
    radius = 400
    pos = None
    ringRadius = None
    pSize = 64
    count = 0
    dTheta = 0
    pSpeed = math.pi/7200
    animationSpeed = .01
    time = 1
    dTime = 1
    actionHeld = False
    mainBoost = True
    leftBoost = False
    rightBoost = False
    pBullets = []
    enemies = []
    pHealth = 30
    waveNum = -1
    newWave = True
    doneWave = True
    waveCounter = 0
    eHealth = 1
    diff = 0
    currentImRect = mainBooster[0].copy()
    currentImRect = currentImRect.get_rect()

    
    width = screen.get_width()
    height = screen.get_height()
    cen = [width/2, height/2]
    pos = [radius*math.cos(theta)+cen[0], radius*math.sin(theta)+cen[1]]
    ringRadius = (height-250)/2
    for i in range(200):
        starValues.append([(255,255,255), (int(random.random()*width), int(random.random()*height), 3, 3)])


def onkey(time, settings, event):
    if not event.type in (pygame.KEYDOWN, pygame.KEYUP):
        return
    key = event.key
    
    global mainBoost
    global leftBoost
    global rightBoost
    global firingCount
    
    global pHealth
    global actionHeld
    
    
    if settings.iskey("left", key):
        mainBoost = False
        leftBoost = event.type == pygame.KEYDOWN
    elif settings.iskey("right", key):
        mainBoost = False
        rightBoost = event.type == pygame.KEYDOWN

    if not leftBoost and not rightBoost:
        mainBoost = True

        
    if settings.iskey("action", key):
        actionHeld = (event.type == pygame.KEYDOWN)

        
    if pHealth <= 0:
        pygame.quit()
        sys.exit()

def handlefiring():
    global firingCount
    global pBullets
    global coeff1
    global coeff2
    firingCount += 1
    
    if actionHeld and firingCount >= firingRate:
        firingCount = 0
        theAngle1 = theta+math.atan(-22/13)
        theAngle2 = theta+math.atan(22/13)
        coeff1 = math.sqrt(400)
        coeff2 = math.sqrt(400)
        pBullets.append(PBullet([pos[0]-coeff1*math.cos(theAngle1), pos[1]-coeff1*math.sin(theAngle1)], theta, pBulletSpeed, laser))
        pBullets.append(PBullet([pos[0]-coeff1*math.cos(theAngle2), pos[1]-coeff1*math.sin(theAngle2)], theta, pBulletSpeed, laser))
    
        
def ontick(timein, settings):
    global time
    global dTime
    dTime = time - timein
    time = timein

    for bullet in eBullets:
        bullet.update()
    for enemy in enemies:
        enemy.update()
    for bullet in pBullets:
        bullet.update()
    
    handlefiring()
    waves()
    movement()
    remove()

def unpause(currenttime):
    global time
    time = currenttime
    
def creategame():
    return Game("polarinvaders", init, onkey, ontick, ondraw, unpause)
    
    
