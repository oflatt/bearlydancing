import random

from .Ship import Ship
from .GridGame import GridGame
from .constants import scrollspeed

# test the difficulty of one subgrid
def simulatedifficulty(subgrid, maxships, settings, pixelsize):
    
    return simulatesmart(subgrid, maxships, settings, pixelsize)


# for each particle, when it hits something, rewind time and try again
# if you get hit by the beginning of the bounding box due to scrolling, give up
def simulatesmart(subgrid, loopcount, settings, pixelsize):
    # time increment will decide how quickly the ship moves, needs to be high enough to escape scroll
    timeincrement = (1000.0/scrollspeed)/5
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
    game = GridGame([subgrid], Ship())

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

    print(wincount)
    print(deathcount)
    return float(wincount)/deathcount
            

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

