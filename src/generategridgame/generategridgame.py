from Game import Game

from .GridGame import GridGame
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction
from FRect import FRect




currentgame = None

def crazysquare(time):
    time = time / 2000
    return (time * time, 0)

def initgridgame(screen):
    global currentgame
    testlavas = [Lava(FRect(.5, .5, .1, .1), crazysquare)]
    currentgame = GridGame([SubGrid(FRect(0, 0, 1, 1), testlavas)])

def onkey(time, settings, event):
    pass

def ontick(time, settings):
    pass

def ondraw(time, settings, screen):
    screen.fill((0,0,0))
    currentgame.draw(time, settings, screen)

def onunpause(time):
    pass

def creategame():
    return Game("gridgame", initgridgame, onkey, ontick, ondraw, onunpause)
