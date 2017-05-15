import pygame, variables, copy, random
from pygame import draw
from random import randint


def makepatch():
    p = pygame.Surface([randint(10, 25), randint(10, 25)])
    p.fill([43, 129, 8])
    

def makegrassland(width, height):
    patches = []
    numofpatches = randint(3, 6)
    for x in range(numofpatches):
        patches.append(makepatch())


