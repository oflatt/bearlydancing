#!/usr/bin/python
import pygame, variables
from Animation import Animation

class Rock():
    collidex = None
    collidey = None
    collidew = None
    collideh = None
    # background range is the range of the player's location that it is drawn behind the player
    background_range = pygame.Rect(0, 0, variables.width * 100, variables.height * 100)
    animations = None
    name = None
    loopanimationsp = False

    def __init__(self, base, x, y, collidesection, name = None):
        # collidesection is a list x y width height all of the arguments are relative to the rock's pos and dimensions
        # width and height of collidesection are multiplied by the width and height of the base
        self.collidesection = collidesection
        if self.collidesection == None:
            self.collidesection = [0, 0, 0, 0]

        # base can be either an image (dictionary), a list of images, an animation, or a list of animations
        #if it is just a single image, put it in an animation
        self.animationnum = 0
        if type(base) == Animation:
            self.animations = [base]
        elif type(base) == dict:
            self.animations = [Animation([base], 1)]
        else:
            #if it's a list of images, wrap them all in animations
            if type(base[0]) == dict:
                for i in range(len(base)):
                    base[i] = Animation([base[i]], 1)
            self.animations = base

        if name != None:
            self.name = name
            self.loopanimationsp = False
        self.x = x
        self.y = y
        self.w = self.animations[0].pics[0]["w"]
        self.h = self.animations[0].pics[0]["h"]
        self.make_mask(True)

    def nextanimation(self):
        if self.animationnum+1 < len(self.animations) or self.loopanimationsp:
            self.animationnum = (self.animationnum + 1) % len(self.animations)

    def draw(self, offset = [0,0]):
        variables.screen.blit(self.animations[self.animationnum].current_frame()["img"], [self.x + offset[0], self.y + offset[1]])

    def make_mask(self, isresetbackgroundrange):
        cs = self.collidesection
        base = self.animations[0].pics[0]
        maskpic = base["img"].copy()
        w = base["img"].get_width()
        h = base["img"].get_height()
        # fill all but the collide section
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, w, cs[1] * h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, cs[0] * w, h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [cs[0] * w + cs[2] * w, 0, w - (cs[0] * w + cs[2] * w), h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, cs[1] * h + cs[3] * h, w, h - (cs[1] * h + cs[3] * h)])
        self.mask = pygame.mask.from_surface(maskpic)

        h = base["h"]
        # by default background range is by the top of the mask, the collision box
        if isresetbackgroundrange:
            if cs == [0, 0, 1, 1]:
                self.background_range = pygame.Rect(0, self.y, variables.width*100, variables.height*100)
            else:
                self.background_range = pygame.Rect(0, self.y + cs[1] * h + cs[3] * (1 / 3) * h,
                                                    variables.width * 100,
                                                    variables.height * 100)

    def scale_by_offset(self, scale):
        s = scale
        self.x *= s
        self.y *= s
        self.x = int(self.x)
        self.y = int(self.y)
        
        # scale base pics to right size
        for anim in self.animations:
            for pic in anim.pics:
                pic["img"] = pygame.transform.scale(pic["img"], [int(pic["w"] * s),
                                                                   int(pic["h"] * s)])
        base = self.animations[0].pics[0]
        
        self.w = base["img"].get_width()
        self.h = base["img"].get_height()

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
        if self.background_range == None:
            self.background_range = pygame.Rect(-1000, -1000, 0, 0)

        self.background_range.x *= s
        self.background_range.y *= s
        self.background_range.width *= s
        self.background_range.height *= s

        self.make_mask(False)
