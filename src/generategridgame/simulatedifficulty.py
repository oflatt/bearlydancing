import random

from .Ship import Ship
from .GridGame import GridGame
from .constants import scrollspeed

# test the difficulty of one subgrid
def simulatedifficulty(subgrid, maxships, settings, pixelsize, numofsimulations):
    s = 0
    for i in range(numofsimulations):
        s = s + simulateonce(subgrid, maxships, settings, pixelsize)

    return s/numofsimulations

def simulateonce(subgrid, maxships, settings, pixelsize):

    # pos is a list that is in pixel coordinates
    # it is the xpos, ypos, xvel, yvel of the ship
    # xvel and yvel are to simulate a particle travelling through the system
    nextposstack = []
    
    currenttimeposstack = []

    movespeed = 0.05/pixelsize
    def randomvelocities(shippos):
        newxvel = random.random()+0.5
        if random.random() < 0.25:
            newxvel = -newxvel
        shippos[2] = newxvel*movespeed
        shippos[3] = (random.random() * 3 - 1.5)*movespeed
        return shippos

    # add maxships to the initial list
    for i in range(maxships):
        currenttimeposstack.append(randomvelocities([4,int((subgrid.rect.h/2)/pixelsize), 0, 0]))
    
    shipcount = 0
    deathcount = 0
    wincount = 0
    game = GridGame([subgrid], Ship())


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

        #spawnchance = 2-(2*(len(nextposstack)+len(currenttimeposstack))/maxships)

        # chance to randomize the velocity of this ship
        if random.random() < 0.2:
            randomvelocities(currentpos)

        currentpos[0] += currentpos[2]
        currentpos[1] += currentpos[3]
        nextposstack.append(currentpos)   

    return float(wincount)/deathcount
