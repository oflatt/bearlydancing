#!/usr/bin/python
import pygame, variables


class Rock():
    collidex = None
    collidey = None
    collidew = None
    collideh = None
    # background range is the range of the player's location that it is drawn behind the player
    background_range = pygame.Rect(0, 0, variables.width * 100, variables.height * 100)
    animation = None

    def __init__(self, base, x, y, collidesection):
        # collidesection is a list x y width height all of the arguments are relative to the rock's pos and dimensions
        # width and height of collidesection are multiplied by the width and height of the base
        self.collidesection = collidesection
        if self.collidesection == None:
            self.collidesection = [0, 0, 0, 0]
        self.base = base
        self.x = x
        self.y = y
        self.w = 2
        self.h = 2
        self.make_mask(True)

    def draw(self):
        if not self.animation == None:
            variables.screen.blit(self.animation.current_frame())
        else:
            variables.screen.blit(self.base["img"], [self.x, self.y])

    def make_mask(self, isresetbackgroundrange):
        cs = self.collidesection
        maskpic = self.base["img"].copy()
        w = self.base["img"].get_width()
        h = self.base["img"].get_height()
        # fill all but the collide section
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, w, cs[1] * h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, cs[0] * w, h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [cs[0] * w + cs[2] * w, 0, w - (cs[0] * w + cs[2] * w), h])
        maskpic.fill(pygame.Color(0, 0, 0, 0), [0, cs[1] * h + cs[3] * h, w, h - (cs[1] * h + cs[3] * h)])
        self.mask = pygame.mask.from_surface(maskpic)

        h = self.base["h"]
        # by default background range is by the top of the mask, the collision box
        if (not cs == [0, 0, 1, 1] and isresetbackgroundrange):
            self.background_range = pygame.Rect(0, self.y + cs[1] * h + cs[3] * (1 / 3) * h,
                                                variables.width * 100,
                                                variables.height * 100)

    def scale_by_offset(self, scale):
        s = scale
        self.x *= s
        self.y *= s
        # scale base pic to right size
        self.base["img"] = pygame.transform.scale(self.base["img"], [int(self.base["w"] * s),
                                                                     int(self.base["h"] * s)])

        if not None == self.animation:
            for x in range(len(self.animation.pics)):
                self.animation.pics[x]["img"] = pygame.transform.scale(self.animation.pics[x]["img"],
                                                                   [int(self.base["w"] * s), int(self.base["h"] * s)])
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
        if self.background_range == None:
            self.background_range = pygame.Rect(-1000, -1000, 0, 0)

        self.background_range.x *= s
        self.background_range.y *= s
        self.background_range.width *= s
        self.background_range.height *= s

        self.make_mask(False)
