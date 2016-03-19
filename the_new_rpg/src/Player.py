#!/usr/bin/python
import pygame, variables

class Player():
    xspeed = 0
    yspeed = 0
    leftpresstime = 0
    rightpresstime = 0
    uppresstime = 0
    downpresstime = 0

    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def draw(self):
        pygame.draw.ellipse(variables.screen, variables.BLACK, [1 + self.xpos, self.ypos, 10, 10], 0)

    def keypress(self, k):
        if k == pygame.K_LEFT:
            self.leftpresstime = pygame.time.get_ticks()
            self.xspeed = -3
        elif k == pygame.K_RIGHT:
            self.rightpresstime = pygame.time.get_ticks()
            self.xspeed = 3
        elif k == pygame.K_UP:
            self.uppresstime = pygame.time.get_ticks()
            self.yspeed = -3
        elif k == pygame.K_DOWN:
            self.downpresstime = pygame.time.get_ticks()
            self.yspeed = 3

    def keyrelease(self, k):
        if k == pygame.K_LEFT:
            self.leftpresstime = 0
            if self.rightpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = 3
        elif k == pygame.K_RIGHT:
            self.rightpresstime = 0
            if self.leftpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = -3
        elif k == pygame.K_UP:
            self.uppresstime = 0
            if self.downpresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = 3
        elif k == pygame.K_DOWN:
            self.downpresstime = 0
            if self.uppresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = 3

    def move(self):
        self.xpos += self.xspeed
        self.ypos += self.yspeed