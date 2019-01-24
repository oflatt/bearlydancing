import pygame, copy

from DestructiveFrozenClass import DestructiveFrozenClass
from FRect import FRect

def zeroposfunction(time):
    return (0, 0)


class Lava(DestructiveFrozenClass):

    # all measurements are fractions of the screen- with of 1 is one screen width
    def __init__(self, rect, posfunction):
        self.rect = rect
        self.posfunction = posfunction
        self._freeze()

    def draw(self, time, settings, screen, posoffset):
        funcoffset = self.posfunction(time)
        screen.fill((180, 0, 0), self.rect.scaledup(screen, offset = (posoffset[0]+funcoffset[0], posoffset[1]+funcoffset[1])))

    def collideswithshipp(self, time, settings, shippos, pixelsize):
        funcoffset = self.posfunction(time)
        posunscaled = (self.rect.x + funcoffset[0], self.rect.y+funcoffset[1])
        
        if posunscaled[0] < shippos[0]+pixelsize and \
           posunscaled[0] + self.rect.w > shippos[0] and \
           posunscaled[1] < shippos[1]+pixelsize and \
           posunscaled[1] + self.rect.h > shippos[1]:
            return True
        else:
            return False
        

    
