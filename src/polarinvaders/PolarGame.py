import math, random


class PolarGame():

    def __init__(self, settings, screen):
        # save reference to screen
        self.oldtime = 1
        self.screen = screen
        self.score = 0
        self.eBullets = []
        self.starValues = []
        self.cen = None
        self.theta = math.pi/2
        self.radius = 400
        self.pos = None
        self.pSize = 64
        self.count = 0
        self.dTheta = 0
        self.pSpeed = math.pi/7200
        self.animationSpeed = .01
        self.dTime = 1
        self.actionHeld = False
        self.mainBoost = True
        self.leftBoost = False
        self.rightBoost = False
        self.pBullets = []
        self.enemies = []
        self.pHealth = 3
        self.waveNum = -1
        self.newWave = True
        self.doneWave = True
        self.waveCounter = 0
        self.eHealth = 1
        self.diff = 0
        self.pBulletSpeed = 7
        self.firingCount = 0
        self.firingRate = 10
        self.currentImRect = None


        self.width = screen.get_width()
        self.cen = [self.width/2, screen.get_height()/2]
        self.pos = [self.radius*math.cos(self.theta)+self.cen[0], self.radius*math.sin(self.theta)+self.cen[1]]
        
        for i in range(200):
            self.starValues.append([(255,255,255), (int(random.random()*self.width), int(random.random()*screen.get_height()), 3, 3)])

        self.gamestate = "menu"

        
