import random

from FRect import FRect

from .simulatedifficulty import simulatedifficulty
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction



def randomgrid(width, safewidth, targetdifficulty, pixelsize):
    print("generating grid with difficulty " + str(targetdifficulty))
    lavacount = int(1.4/targetdifficulty)
    lavas = []

    def addlava():
        newFRect = FRect(0,0,random.random()/2,random.random()/2)
        centerx = random.uniform(safewidth+newFRect.w/2, width-newFRect.w/2)
        centery = random.uniform(newFRect.h/2, 1-newFRect.h/2)
        newFRect.center(centerx, centery)
        lavas.append(Lava(newFRect, zeroposfunction))

    def getdifficulty():
        return simulatedifficulty(SubGrid(FRect(0,0,width,1), lavas), 500, None, pixelsize)
    
    for i in range(lavacount):
        addlava()

    difficulty = getdifficulty()
    if difficulty > targetdifficulty:
        newdifficulty = difficulty
        
        # add lavas until it goes past the target
        while newdifficulty > targetdifficulty:
            print("add lava")
            addlava()
            difficulty = newdifficulty
            newdifficulty = getdifficulty()

            
    elif difficulty < targetdifficulty:
        # remove lavas until it goes past the target
        newdifficulty = difficulty

        while newdifficulty < targetdifficulty and len(lavas)>0:
            print("remove lava")
            lavas.pop()
            difficulty = newdifficulty
            newdifficulty = getdifficulty()

            if len(lavas)==0:
                print("add lava because there are none")
                addlava()

    return SubGrid(FRect(0,0,width, 1), lavas)
