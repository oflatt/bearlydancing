import random

from variables import devprint

from .Ship import Ship
from .GridGame import GridGame
from .constants import basescrollspeed

# test the difficulty of one subgrid
def simulatedifficulty(subgrid, maxships, settings, pixelsize):
    
    result = simulatesmart(subgrid, maxships, settings, pixelsize)
    devprint(result)

    return result


# for each particle, when it hits something, rewind time and try again
# if you get hit by the beginning of the bounding box due to scrolling, give up
def simulatesmart(subgrid, loopcount, settings, pixelsize):
    # time increment will decide how quickly the ship moves, needs to be high enough to escape scroll
    timeincrement = (1000.0/basescrollspeed)/5
    maxdeaths = int(subgrid.rect.w/pixelsize)*4
    rightprobabilities = (0.7, 0.1, 0.1, 0.1)
    leftprobabilities = (0.1, 0.7, 0.1, 0.1)
    upprobabilities = (0.1, 0.1, 0.7, 0.1)
    downprobabilities = (0.1, 0.1, 0.1, 0.7)
    rightcollisionprobabilitieslist = (upprobabilities, downprobabilities)
    leftcollisionprobabilitieslist = (rightprobabilities, upprobabilities, downprobabilities)
    upcollisionprobabilitieslist = (rightprobabilities, downprobabilities)
    downcollisionprobabilitieslist = (rightprobabilities, upprobabilities)

    
    deathcount = 0
    wincount = 0
    game = GridGame([subgrid], Ship(), scrollgrowthrate = 0)

    # initialize variables used in the loop
    # positions in pixel coordinates
    oldx = None
    oldy = None
    xpos = None
    ypos = None
    time = None
    deaths = None

    for i in range(loopcount):
        deaths = 0
        xpos = 2
        ypos = int((1/pixelsize - 1) * i/loopcount)
        
        oldx = xpos
        oldy = ypos
        
        movementprobabilities = rightprobabilities
        time = 0

        while True:

            # if you hit something, try again
            if game.gameoverp(time, settings, pixelsize, shippospixels = (xpos, ypos)):
                deathcount += 1
                deaths += 1
                if deaths > maxdeaths:
                    break
                probindex = random.randint(0, 2)
                if oldx > xpos:
                    movementprobabilities = random.choice(rightcollisionprobabilitieslist)
                elif oldx < xpos:
                    movementprobabilities = random.choice(leftcollisionprobabilitieslist)
                elif oldy > ypos:
                    movementprobabilities = random.choice(downcollisionprobabilitieslist)
                elif oldy < ypos:
                    movementprobabilities = random.choice(upcollisionprobabilitieslist)
                # also a chance to go left
                if random.random() < 0.05:
                    movementprobabilities = leftprobabilities

                
                
                xpos = oldx
                ypos = oldy
                time -= timeincrement
                
        
            # win if made to the end
            if xpos*pixelsize >= subgrid.rect.w:
                # if it has, it made it
                wincount += 1
                break

            # movement
            oldx = xpos
            oldy = ypos
            if random.random() < movementprobabilities[0]:
                xpos += 1
            if random.random() < movementprobabilities[1]:
                xpos -= 1
            if random.random() < movementprobabilities[2]:
                ypos += 1
            if random.random() < movementprobabilities[3]:
                ypos -= 1
            time += timeincrement

    devprint(wincount)
    devprint(deathcount)
    return float(wincount)/deathcount
            
