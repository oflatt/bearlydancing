import random, math

from FRect import FRect
from variables import devprint

from .simulatedifficulty import simulatedifficulty
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction


maxiterations = 10

def randomgrid(width, safewidth, targetdifficulty, pixelsize):
    devprint("generating grid with difficulty " + str(targetdifficulty))
    
    # an integer representation of the difficulty
    lavacount = int(math.log(0.5/targetdifficulty, 2))
    lavas = []

    def adddifficulty():
        # chance to add wave of projectiles
        if random.random() < 0.2:
            projectilesize = 0.1
            spacingx = random.uniform(-0.3, 0.3)
            spacingy = random.uniform(-0.3, 0.3)
            number = random.randint(2, 5)
            ypos = random.randint(...

        
        newFRect = FRect(0,0,random.uniform(0.2, 0.4),random.uniform(0.2, 0.4))
        centerx = random.uniform(safewidth+newFRect.w/2, width-newFRect.w/2)
        centery = random.uniform(newFRect.h/2, 1-newFRect.h/2)
        newFRect.center(centerx, centery)
        lavas.append(Lava(newFRect, zeroposfunction))
        
    def removedifficulty():
        lavas.pop(random.randrange(len(lavas)))
        
    def getdifficulty():
        return simulatedifficulty(SubGrid(FRect(0,0,width,1), lavas), 100, None, pixelsize)

    def withindifficultyp(diff):
        return abs(targetdifficulty-diff) < targetdifficulty/5
    
    for i in range(lavacount):
        adddifficulty()

    difficulty = getdifficulty()
    newdifficulty = difficulty
    iterations = 0
        
    # add lavas until it goes past the target
    while not withindifficultyp(newdifficulty) and iterations < maxiterations:
        if newdifficulty > targetdifficulty:
            devprint("add lava")
            adddifficulty()
        else:
            devprint("remove lava")
            devprint("lavas: " + str(len(lavas)))
            removedifficulty()
        difficulty = newdifficulty
        newdifficulty = getdifficulty()
        iterations += 1


    return SubGrid(FRect(0,0,width, 1), lavas)
