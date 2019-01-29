import random

from .Ship import Ship
from .GridGame import GridGame
from .constants import scrollspeed

# test the difficulty of one subgrid
def simulatedifficulty(subgrid, maxships, settings, pixelsize, numofsimulations):
    s = 0
    for i in range(8):
        s = s + simulateonce(subgrid, maxships, settings, pixelsize)

    return s/numofsimulations

def simulateonce(subgrid, maxships, settings, pixelsize):

    # pos is in pixel coordinates
    nextposstack = []
    
    currenttimeposstack = [(int((subgrid.rect.h/2)/pixelsize), 4)]
    shipcount = 0
    deathcount = 0
    wincount = 0
    game = GridGame([subgrid], Ship())

    spawnupchance = 0.35
    spawndownchance = 0.35
    spawnbackchance = 0.2
    stayputchance = 0.5
    spawnforwardchance = 0.7
    
    # how much to increment time when moving- make it so that there is a good chance to continue moving forward
    timeincrement = (1000.0/scrollspeed)/2
    
    # all ships in currenttimesposstack are being simulated at time time
    time = 0
    
    
    while len(nextposstack) > 0 or len(currenttimeposstack) > 0:
    
        if len(currenttimeposstack) == 0:
            currenttimeposstack = nextposstack
            nextposstack = []
            time += timeincrement
        

        currentpos = currenttimeposstack.pop()
        shipcount += 1
        
        if game.gameoverp(time, settings, pixelsize, shippospixels = currentpos):
            deathcount += 1
            continue
        
        # also make sure the ship has not gone past the subgrid
        if currentpos[0]*pixelsize >= subgrid.rect.w:
            # if it has, it made it
            wincount += 1
            continue

        maxshipschance = 2-(2*(len(nextposstack)+len(currenttimeposstack))/maxships)
        
        if random.random() < spawnupchance*maxshipschance:
            nextposstack.append((currentpos[0], currentpos[1]-1))
        if random.random() < spawndownchance*maxshipschance:
            nextposstack.append((currentpos[0], currentpos[1]+1))
        if random.random() < spawnforwardchance*maxshipschance:
            nextposstack.append((currentpos[0]+1, currentpos[1]))
        if random.random() < spawnbackchance*maxshipschance:
            nextposstack.append((currentpos[0]-1, currentpos[1]-1))

    return float(wincount)/deathcount
