from Game import Game
from .GrowGame import GrowGame


def initgame(settings, screen):
    if settings.getgamedata("growgame") == None:
        settings.setgamedata("growgame", GrowGame())

    
def onkeydown(outsidetime, settings, key):
    pass

def onkeyup(outsidetime, settings, key):
    pass

    
def ontick(outsidetime, settings):
    pass
        

def ondraw(outsidetime, settings, screen):
    settings.getgamedata("growgame").draw(outsidetime, settings, screen)

def onpause(time):
    pass
    
def onunpause(time):
    pass

def creategame():
    return Game("growgame", initgame, onkeydown, onkeyup, ontick, ondraw, onpause, onunpause)
