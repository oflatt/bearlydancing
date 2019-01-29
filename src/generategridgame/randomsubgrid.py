import random

from FRect import FRect

from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction



def randomgrid(width, lavacount, targetdifficulty):
    lavas = []
    for i in lavacount:
        newFRect = FRect(0,0,random.random()/2,random.random()/2)
        newFRect.center(random.random()*width, random.random())
        lavas.append(Lava(newFRect, zeroposfunction))
