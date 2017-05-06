import pygame, variables, copy, random
from pygame import draw
from random import randint



def makepatch():
    p = pygame.Surface([randint(10, 25), randint(10, 25)])
    p.fill([43, 129, 8])


def makegrassland():
    basewidth = variables.basemapsize
    width = random.choice(basewidth, basewidth*2, basewidth*3)
    height = randint(basewidth, basewidth, basewidth*2)

