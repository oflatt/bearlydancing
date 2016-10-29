#!/usr/bin/python
import pygame, variables

class Rock():
    collidex = None
    collidey = None
    collidew = None
    collideh = None
    #foreground range is the range of the player's location that it is drawn in the foreground
    foreground_range = pygame.Rect(0,0,0,0)

    def __init__(self, base, x, y, c):
        #base is a png picture
        self.base = base
        self.x = x
        self.y = y
        #iscollideable is a bool
        self.iscollideable = c
        self.w = 2
        self.h = 2
        self.mask = pygame.mask.from_surface(self.base["img"])

    def draw(self):
        variables.screen.blit(self.base["img"], [self.x, self.y])

    def scale_by_offset(self, scale):
        s = scale
        self.x *= s
        self.y *= s
        #scale base pic to right size
        self.base["img"] = pygame.transform.scale(self.base["img"], [int(self.base["w"]*s),
                                                                     int(self.base["h"]*s)])
        self.w = self.base["img"].get_width()
        self.h = self.base["img"].get_height()
        if self.collidex == None:
            self.collidex = self.x
        else:
            self.collidex *= s

        if self.collidey == None:
            self.collidey = self.y
        else:
            self.collidey *= s
        if self.collidew == None:
            self.collidew = self.w
        else:
            self.collidew *= s

        if self.collideh == None:
            self.collideh = self.h
        else:
            self.collideh *= s
        self.foreground_range.x *= s
        self.foreground_range.y *= s
        self.foreground_range.width *= s
        self.foreground_range.height *= s
        self.mask = pygame.mask.from_surface(self.base["img"])