import random, math

from FRect import FRect
from variables import devprint

from .simulatedifficulty import simulatedifficulty
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction


maxiterations = 10

def randomgrid(width, safewidth, targetdifficulty, pixelsize):
    devprint("generating grid with difficulty " + str(targetdifficulty))
    lavacount = int(math.log(0.5/targetdifficulty, 2))
    lavas = []

    def addlava():
        newFRect = FRect(0,0,random.uniform(0.2, 0.4),random.uniform(0.2, 0.4))
        centerx = random.uniform(safewidth+newFRect.w/2, width-newFRect.w/2)
        centery = random.uniform(newFRect.h/2, 1-newFRect.h/2)
        newFRect.center(centerx, centery)
        lavas.append(Lava(newFRect, zeroposfunction))

    def getdifficulty():
        return simulatedifficulty(SubGrid(FRect(0,0,width,1), lavas), 150, None, pixelsize)

    def withindifficultyp(diff):
        return abs(targetdifficulty-diff) < targetdifficulty/5
    
    for i in range(lavacount):
        addlava()

    difficulty = getdifficulty()
    newdifficulty = difficulty
    iterations = 0
        
    # add lavas until it goes past the target
    while not withindifficultyp(newdifficulty) and iterations < maxiterations:
        if newdifficulty > targetdifficulty:
            devprint("add lava")
            addlava()
        else:
            devprint("remove lava")
            devprint("lavas: " + str(len(lavas)))
            lavas.pop(random.randrange(len(lavas)))
        difficulty = newdifficulty
        newdifficulty = getdifficulty()
        iterations += 1


    return SubGrid(FRect(0,0,width, 1), lavas)
