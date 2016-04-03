#!/usr/bin/python
import pygame, variables, maps

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

    def draw(self): #movement is combination of top down scrolling and free range
        m = maps.current_map
        mw = m.base.get_width()
        mh = m.base.get_height()
        if self.xpos >= variables.hh and self.xpos <= (mw - variables.hh):#If in scrolling area
            drawx = variables.hh #middle of screen
        elif self.xpos > (mw - variables.hh): #if on right side
            drawx = self.xpos - (mw - variables.height) #normal x pos adjusted for scrolling area
        else:
            drawx = self.xpos #otherwise make the coordinates normal
        if self.ypos >= variables.hh and self.ypos <= (mh - variables.hh): #same logic for y pos
            drawy = variables.hh
        elif self.ypos > (mh - variables.hh):
            drawy = self.ypos - (mh - variables.height) #mh - variables.height is the height of the scrolling area
        else:
            drawy = self.ypos
        pygame.draw.ellipse(variables.screen, variables.RED, [drawx, drawy, 20, 20], 0)

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
                self.yspeed = -3

    #moves with collision detections
    def move(self):
        movedxpos = self.xpos + self.xspeed
        movedypos = self.ypos + self.yspeed
        iscollisionx = False
        iscollisiony= False
        m = maps.current_map
        t = m.terrain
        numofrocks = len(t)

        #checks if the moved position on within the coordinates of a single rock
        def collisioncheck(arock, x, y):
            return arock.iscollideable and x>=arock.x and x<=(arock.x + arock.w) \
                   and y>=arock.y and y<=(arock.y + arock.h)

        #collision detection for the moved x pos with the unmoved y pos
        for x in range(0, numofrocks-1):
            r = t[x]
            if collisioncheck(r, movedxpos, self.ypos):
                iscollisionx = True
                x = numofrocks
        
        #collision detection for the moved y pos with the unmoved x pos
        for x in range(0, numofrocks-1):
            r = t[x]
            if collisioncheck(r, self.xpos, movedypos):
                iscollisiony = True
                x = numofrocks

        if not iscollisionx:
            self.xpos = movedxpos

        if not iscollisiony:
            self.ypos = movedypos