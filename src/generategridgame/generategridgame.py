import math, pygame, sys

from Game import Game
from FRect import FRect

from .GridGame import GridGame
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction
from .Ship import Ship
from .simulatedifficulty import simulatedifficulty


def crazysquare(time):
    
    time = (time / 1000.0) % 2

    if time < 1:
        return (0, -time/4.0)
    else:
        return (0, -(1 - (time-1))/4.0)


# first test simulateddifficulty
testlavas = [Lava(FRect(.5, .5, .5, .5), crazysquare)]

print(simulatedifficulty(SubGrid(FRect(0,0,1.5,1), testlavas), 1000, None, 0.05))


# all coordinates are expressed as a fraction of screen height

currentgame = None
pixelsize = 0.1


    
def initgridgame(screen):
    global currentgame
    testlavas = [Lava(FRect(.5, .5, .1, .1), crazysquare)]
    currentgame = GridGame([SubGrid(FRect(0, 0, 1, 1), testlavas)], Ship())

def onkey(time, settings, event):
    global currentgame
    currentgame = currentgame.onkey(time, settings, event, pixelsize)

def ontick(time, settings):
    global currentgame
    currentgame = currentgame.ontick(time, settings)
    
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
