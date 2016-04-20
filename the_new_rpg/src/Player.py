#!/usr/bin/python
import pygame, variables, maps, graphics, stathandeling
from Dancer import Dancer

class Player(Dancer):
    xspeed = 0
    yspeed = 0
    leftpresstime = 0
    rightpresstime = 0
    uppresstime = 0
    downpresstime = 0
    current_frame = graphics.honey_right1
    normal_width = current_frame.get_width()
    normal_height = current_frame.get_height()
    xpos = 0
    ypos = 0
    lastxupdate = 0
    lastyupdate = 0
    storyprogress = 1

    def teleport(self, x, y):
        self.xpos = x
        self.ypos = y

    def draw(self): #movement is combination of top down scrolling and free range
        m = maps.current_map
        mw = m.finalimage.get_width()
        mh = m.finalimage.get_height()
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
        self.move()
        t = variables.current_time
        s = variables.playerspeed * variables.scaleoffset
        if k == pygame.K_LEFT or k == pygame.K_a:
            self.leftpresstime = variables.current_time
            self.xspeed = -s
            self.lastxupdate = t
        elif k == pygame.K_RIGHT or k == pygame.K_d:
            self.rightpresstime = variables.current_time
            self.lastxupdate = t
            self.xspeed = s
        elif k == pygame.K_UP or k == pygame.K_w:
            self.uppresstime = variables.current_time
            self.yspeed = -s
            self.lastyupdate = t
        elif k == pygame.K_DOWN or k == pygame.K_s:
            self.downpresstime = variables.current_time
            self.yspeed = s
            self.lastyupdate = t

    def keyrelease(self, k):
        self.move()
        s = variables.playerspeed * variables.scaleoffset
        t = variables.current_time
        if k == pygame.K_LEFT or k == pygame.K_a:
            self.leftpresstime = 0
            self.lastxupdate = t
            if self.rightpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = s
        elif k == pygame.K_RIGHT or k == pygame.K_d:
            self.rightpresstime = 0
            self.lastxupdate = t
            if self.leftpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = -s
        elif k == pygame.K_UP or k == pygame.K_w:
            self.lastyupdate = t
            self.uppresstime = 0
            if self.downpresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = s
        elif k == pygame.K_DOWN or k == pygame.K_s:
            self.lastyupdate = t
            self.downpresstime = 0
            if self.uppresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = -s

    #moves with collision detections
    def move(self):
        t = variables.current_time
        #calculate moved positions
        xtime_factor = t-self.lastxupdate
        ytime_factor = t-self.lastyupdate
        movedxpos = self.xpos + self.xspeed*xtime_factor
        movedypos = self.ypos + self.yspeed*ytime_factor

        #collision detection
        iscollisionx = False
        iscollisiony= False
        m = maps.current_map
        t = m.terrain
        numofrocks = len(t)
        s = variables.scaleoffset #used because actual rocks are not really scaled

        #checks if the player's right side collides with a rock
        def collisioncheck(arock, x, y):
            return arock.iscollideable and (x+self.normal_width)>=arock.x*s and x<=(arock.x*s + arock.w*s) \
                   and (y+self.normal_height)>=arock.y*s and y<=(arock.y*s + arock.h*s)

        if not self.xspeed == 0:
            #collision detection for the moved x pos with the unmoved y pos
            for x in range(0, numofrocks):
                r = t[x]
                if collisioncheck(r, movedxpos, self.ypos):
                    iscollisionx = True
                    break

        if not self.yspeed == 0:
            #collision detection for the moved y pos with the unmoved x pos
            for x in range(0, numofrocks):
                r = t[x]
                if collisioncheck(r, self.xpos, movedypos):
                    iscollisiony = True
                    break

        if not iscollisionx:
            self.xpos = movedxpos

        if not iscollisiony:
            self.ypos = movedypos
        self.lastxupdate = variables.current_time
        self.lastyupdate = variables.current_time

    def scale_by_offset(self):
        self.current_frame = graphics.honey_right1
        self.current_frame = pygame.transform.scale(self.current_frame,
                                                    [int(self.current_frame.get_width()*variables.scaleoffset),
                                                     int(self.current_frame.get_height()*variables.scaleoffset)])
        self.normal_width = self.current_frame.get_width()
        self.normal_height = self.current_frame.get_height()

    def ismoving(self):
        return not (self.xspeed==0 and self.yspeed==0)

    def heal(self):
        self.health = stathandeling.max_health(self.lv)

    def change_of_state(self):
        self.downpresstime = 0
        self.uppresstime = 0
        self.leftpresstime = 0
        self.rightpresstime = 0
        self.xspeed = 0
        self.yspeed = 0
