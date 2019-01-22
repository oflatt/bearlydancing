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

    
