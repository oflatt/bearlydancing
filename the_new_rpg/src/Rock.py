#!/usr/bin/python
import pygame, variables

class Rock():
    def __init__(self, base, x, y, c):
        #base is a png picture
        self.base = base
        self.x = x
        self.y = y
        #iscollideable is a bool
        self.iscollideable = c

    def draw(self):
        variables.screen.blit(self.base, [self.x, self.y])