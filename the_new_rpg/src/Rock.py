#!/usr/bin/python
import pygame, variables

class Rock():
    def __init__(self, base, x, y):
        #base is a png picture
        self.base = base
        self.x = x
        self.y = y

    def draw(self):
        variables.screen.blit(self.base, [self.x, self.y])