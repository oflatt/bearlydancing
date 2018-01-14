#!/usr/bin/python
import pygame, variables
from Animation import Animation
from graphics import GR, getpic, getmask

class Rock():

    def __init__(self, base, x, y, collidesection, name = None):

        self.animations = None

        # base can be either an imagename, a list of imagenames, an animation, or a list of animations
        #if it is just a single image, put it in an animation
        self.animationnum = 0
        if type(base) == Animation:
            self.animations = [base]
        elif type(base) == str:
            self.animations = [Animation([base], 1)]
        else:
            #if it's a list of images, wrap them all in animations
            if type(base[0]) == str:
                for i in range(len(base)):
                    base[i] = Animation([base[i]], 1)
            self.animations = base

        self.name = name
        self.loopanimationsp = False

        self.collidex = x
        self.collidey = y
        
        self.x = x
        self.y = y
        self.w = GR[self.animations[0].pics[0]]["w"]
        self.h = GR[self.animations[0].pics[0]]["h"]
        self.draw_scale = 1

        # used to keep track of if it was drawn for backgroundrange
        self.drawnp = False

        # collidesection is a list x y width height all of the arguments are relative to the rock's pos and dimensions
        # width and height of collidesection are multiplied by the width and height of the base
        self.collidesection = collidesection
        if self.collidesection == None:
            self.collidesection = [0, 0, 0, 0]
        else:
            self.collidesection = self.collidesection.copy()
            self.collidesection[0] *= self.w
            self.collidesection[1] *= self.h
            self.collidesection[2] *= self.w
            self.collidesection[3] *= self.h
        for i in range(len(self.collidesection)):
            self.collidesection[i] = int(self.collidesection[i])
        self.collidesection = tuple(self.collidesection)
        self.set_backgroundrange()


    def nextanimation(self):
        if self.animationnum+1 < len(self.animations) or self.loopanimationsp:
            self.animationnum = (self.animationnum + 1) % len(self.animations)

    def draw(self, offset = [0,0]):
        p = getpic(self.animations[self.animationnum].current_frame(), variables.compscale)
        drawx = self.x * variables.compscale + offset[0]
        drawy = self.y * variables.compscale + offset[1]
        variables.screen.blit(p, [drawx, drawy])

    # background range is the range of the player's location that it is drawn behind the player
    def set_backgroundrange(self):
        cs = self.collidesection
        h = GR[self.animations[0].pics[0]]["h"]
        if cs == (0, 0, self.w, self.h):
            self.background_range = pygame.Rect(0, self.y, 9999999, 9999999)
        else:
            self.background_range = pygame.Rect(0, int(self.y + cs[1] + cs[3] * (1 / 3)), 9999999, 9999999)

    def get_mask(self):
        return getmask(self.animations[0].pics[0], self.collidesection)
        
