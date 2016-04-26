#!/usr/bin/python
import pygame, variables, maps, graphics, stathandeling
from Dancer import Dancer
from Animation import Animation

class Player(Dancer):
    xspeed = 0
    yspeed = 0
    leftpresstime = 0
    rightpresstime = 0
    uppresstime = 0
    downpresstime = 0
    normal_width = 10
    normal_height = 10
    xpos = 0
    ypos = 0
    lastxupdate = 0
    lastyupdate = 0
    storyprogress = 1

    #animation
    left_animation = Animation([graphics.left_honey1, graphics.left_honey2, graphics.left_honey3], 100)
    right_animation = Animation([graphics.honey_right0, graphics.honey_right1,
                                 graphics.honey_right2, graphics.honey_right3], 100)
    up_animation = Animation([graphics.back_honey0, graphics.back_honey1,
                              graphics.back_honey2, graphics.back_honey3], 100)
    down_animation = Animation([graphics.front_honey0, graphics.front_honey1,
                                graphics.front_honey2, graphics.front_honey3], 100)
    current_animation = left_animation

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
        variables.screen.blit(self.current_pic_scaled(), [drawx, drawy])

    def change_animation(self):
        if self.xspeed == 0:
            if self.yspeed < 0:
                self.current_animation = self.up_animation
            elif self.yspeed > 0:
                self.current_animation = self.down_animation
        elif self.xspeed < 0:
            self.current_animation = self.left_animation
        elif self.xspeed > 0:
            self.current_animation = self.right_animation
        self.current_animation.reset()

    def keypress(self, k):
        self.move()
        t = variables.current_time
        s = variables.playerspeed * variables.scaleoffset
        if k == pygame.K_LEFT or k == pygame.K_a:
            self.leftpresstime = variables.current_time
            self.xspeed = -s
            self.lastxupdate = t
        if k == pygame.K_RIGHT or k == pygame.K_d:
            self.rightpresstime = variables.current_time
            self.lastxupdate = t
            self.xspeed = s
        if k == pygame.K_UP or k == pygame.K_w:
            self.uppresstime = variables.current_time
            self.yspeed = -s
            self.lastyupdate = t
        if k == pygame.K_DOWN or k == pygame.K_s:
            self.downpresstime = variables.current_time
            self.yspeed = s
            self.lastyupdate = t
        self.change_animation()

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
        self.change_animation()

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

    def current_pic_scaled(self): #returns the current pic to display
        if self.leftpresstime == 0 and self.rightpresstime == 0 and \
            self.uppresstime == 0 and self.downpresstime == 0:
            c = self.current_animation.pics[0]
        else:
            c = self.current_animation.current_frame()
        c = pygame.transform.scale(c,
                                    [int(c.get_width()*variables.scaleoffset),
                                     int(c.get_height()*variables.scaleoffset)])
        return c

    def scale_by_offset(self):
        self.normal_width = self.current_pic_scaled().get_width()
        self.normal_height = self.current_pic_scaled().get_height()

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
