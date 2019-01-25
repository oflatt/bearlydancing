
from .GridGame import GridGame

# test the difficulty of one subgrid
def simulatedifficulty(subgrid, maxships, pixelsize):
    numrows = int(subgrid.rect.h/pixelsize)
    numcols = int(subgrid.rect.w / pixelsize)

    # pos is in pixel coordinates
    posstack = [int((subgrid.rect.h/2)/pixelsize)]
    shipcount = 0
    Game = 
    while shipcount < maxships and len(posstack > 0):
        
