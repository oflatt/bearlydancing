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
    direction = None

    for i in range(loopcount):
        direction = (1, 0)
        deaths = 0
        xpos = 2
        ypos = int((1/pixelsize - 1) * i/loopcount)
        
        oldx = xpos
        oldy = ypos
        
        time = 0

        while True:

            # if you hit something, try again
            if game.gameoverp(time, settings, pixelsize, shippospixels = (xpos, ypos)):
                deathcount += 1
                deaths += 1
                if deaths > maxdeaths:
                    break

                # was moving left or right
                if direction[1] == 0:
                    if random.random() < 0.4:
                        direction = (-direction[0], 0)
                    else:
                        direction = (0, random.choice((-1, 1)))
                                    
                elif direction[0] == 0:
                    if random.random() < 0.1:
                        direction = (-1, 0)
                    elif random.random() < 0.7:
                        direction = (1, 0)
                    else:
                        direction = (0, -direction[1]) # opposite verticle directio
                
                
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
            xpos += direction[0]
            ypos += direction[1]
            time += timeincrement

    devprint(wincount)
    devprint(deathcount)
    if deathcount == 0:
        return wincount
    else:
        return float(wincount)/deathcount
            
