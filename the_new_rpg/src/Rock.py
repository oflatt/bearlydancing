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
        self.w = base.get_width()
        self.h = base.get_height()

    def draw(self):
        variables.screen.blit(self.base, [self.x, self.y])

    def scale_by_offset(self, scale):
        s = scale
        self.x *= s
        self.y *= s
        #scale base pic to right size
        self.base = pygame.transform.scale(self.base, [self.base.get_width()*s, self.base.get_height*s])
        self.w = self.base.get_width()
        self.h = self.base.get_height()