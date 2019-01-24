import math, pygame, sys

from Game import Game
from FRect import FRect

from .GridGame import GridGame
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction
from .Ship import Ship


# all coordinates are expressed as a fraction of screen height

currentgame = None
pixelsize = 0.1

def crazysquare(time):
    time = (time / 2000) % math.sqrt(0.5)
    return (time * time, 0)

def initgridgame(screen):
    global currentgame
    testlavas = [Lava(FRect(.5, .5, .1, .1), crazysquare)]
    currentgame = GridGame([SubGrid(FRect(0, 0, 1, 1), testlavas)], Ship())

def onkey(time, settings, event):
    global currentgame
    currentgame = currentgame.onkey(time, settings, event, pixelsize)

def ontick(time, settings):
    
    if currentgame.gameoverp(time, settings, pixelsize):
        pygame.quit()
        sys.exit()
        

def ondraw(time, settings, screen):
    screen.fill((0,0,0))
    currentgame.draw(time, settings, screen, pixelsize)

def onunpause(time):
    pass

def creategame():
    return Game("gridgame", initgridgame, onkey, ontick, ondraw, onunpause)
