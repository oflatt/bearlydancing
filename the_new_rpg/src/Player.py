#!/usr/bin/python
import pygame, variables, maps, graphics

class Player():
    xspeed = 0
    yspeed = 0
    leftpresstime = 0
    rightpresstime = 0
    uppresstime = 0
    downpresstime = 0
    current_frame = graphics.honey_right1
    normal_width = current_frame.get_width()
    normal_height = current_frame.get_height()

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
        variables.screen.blit(self.current_frame, [drawx, drawy])

    def keypress(self, k):
        s = variables.playerspeed
        if k == pygame.K_LEFT or k == pygame.K_a:
            self.leftpresstime = pygame.time.get_ticks()
            self.xspeed = -s
        elif k == pygame.K_RIGHT or k == pygame.K_d:
            self.rightpresstime = pygame.time.get_ticks()
            self.xspeed = s
        elif k == pygame.K_UP or k == pygame.K_w:
            self.uppresstime = pygame.time.get_ticks()
            self.yspeed = -s
        elif k == pygame.K_DOWN or k == pygame.K_s:
            self.downpresstime = pygame.time.get_ticks()
            self.yspeed = s

    def keyrelease(self, k):
        if k == pygame.K_LEFT or k == pygame.K_a:
            self.leftpresstime = 0
            if self.rightpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = 3
        elif k == pygame.K_RIGHT or k == pygame.K_d:
            self.rightpresstime = 0
            if self.leftpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = -3
        elif k == pygame.K_UP or k == pygame.K_w:
            self.uppresstime = 0
            if self.downpresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = 3
        elif k == pygame.K_DOWN or k == pygame.K_s:
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

        #checks if the player's right side collides with a rock
        def collisioncheck(arock, x, y):
            return arock.iscollideable and (x+self.normal_width)>=arock.x and x<=(arock.x + arock.w) \
                   and (y+self.normal_height)>=arock.y and y<=(arock.y + arock.h)

        if not self.xspeed == 0:
            #collision detection for the moved x pos with the unmoved y pos
            for x in range(0, numofrocks):
                r = t[x]
                if collisioncheck(r, movedxpos, self.ypos):
                    iscollisionx = True
                    x = numofrocks

        if not self.yspeed == 0:
            #collision detection for the moved y pos with the unmoved x pos
            for x in range(0, numofrocks):
                r = t[x]
                if collisioncheck(r, self.xpos, movedypos):
                    iscollisiony = True
                    x = numofrocks

        if not iscollisionx:
            self.xpos = movedxpos

        if not iscollisiony:
            self.ypos = movedypos