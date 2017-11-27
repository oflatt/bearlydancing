#!/usr/bin/python
import pygame, variables, maps, stathandeling
from graphics import GR
from Dancer import Dancer
from Animation import Animation
from pygame import Rect

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
    drawx = 0
    drawy = 0
    mapdrawx = 0
    mapdrawy = 0
    lastxupdate = 0
    lastyupdate = 0
    storyprogress = 0

    #animation
    left_animation = Animation([GR["honeyside3"], GR["honeyside4"], GR["honeyside3"], GR["honeyside4"]], 200)
    right_animation = Animation([GR["honeyside0"], GR["honeyside1"],
                                 GR["honeyside0"], GR["honeyside2"]], 200)
    down_animation = Animation([GR["honeyback3"], GR["honeyback4"],
                                GR["honeyback3"], GR["honeyback5"]], 200)
    up_animation = Animation([GR["honeyback0"], GR["honeyback1"],
                              GR["honeyback0"], GR["honeyback2"]], 200)
    current_animation = right_animation

    def teleport(self, x, y):
        if not x == "same":
            self.xpos = x
        if not y == "same":
            self.ypos = y

    def update_drawpos(self):
        x = self.xpos
        y = self.ypos
        m = maps.current_map
        w = m.finalimage.get_width()
        h = m.finalimage.get_height()
        pwidth = self.normal_width
        pheight = self.normal_height
        hpheight = pheight/2
        hpwidth = pwidth/2
        if w <= variables.width:
            # if the map fits in the screen, no scrolling needed
            self.drawx = x
            self.mapdrawx = 0
        elif x < variables.hw - hpwidth:  # if it is in the left side of the map
            self.mapdrawx = 0  # do not scroll the map at all
            self.drawx = x
        elif x > (w - variables.hw - hpwidth):  # if it is on the right side of the map
            self.mapdrawx = w - variables.width  # set it to the maximum scroll
            self.drawx = x - (w-variables.width)
        else:
            # otherwise, scroll it by pos (accounting for the initial non-scolling area)
            self.mapdrawx = x - variables.hw + hpwidth
            self.drawx = variables.hw - hpwidth

        if h <= variables.height:
            self.drawy = y
            self.mapdrawy = 0
        elif y < variables.hh - hpheight:  # same but for y pos
            self.mapdrawy = 0
            self.drawy = y
        elif y > (h - variables.hh - hpheight):
            self.mapdrawy = h - variables.height
            self.drawy = y - (h-variables.height)
        else:
            self.mapdrawy = y - variables.hh + hpheight
            self.drawy = variables.hh - hpheight

        # then add the map's x offset for drawing small maps in the middle
        self.drawx += m.screenxoffset
        self.mapdrawx -= m.screenxoffset
        #round to nearest pixel
        self.mapdrawx = int(self.mapdrawx)
        self.mapdrawy = int(self.mapdrawy)

    def draw(self): #movement is combination of top down scrolling and free range
        self.current_pic_scaled()
        variables.screen.blit(self.current_display, [self.drawx, self.drawy])

    def change_animation(self):
        oldanimation = self.current_animation
        if self.xspeed == 0:
            if self.yspeed < 0:
                self.current_animation = self.up_animation
            elif self.yspeed > 0:
                self.current_animation = self.down_animation
        elif self.xspeed < 0:
            self.current_animation = self.left_animation
        elif self.xspeed > 0:
            self.current_animation = self.right_animation
        if oldanimation != self.current_animation:
            self.current_animation.reset()

    def keypress(self, k):
        self.move()
        t = variables.settings.current_time
        s = variables.playerspeed * variables.scaleoffset
        if k in variables.settings.leftkeys:
            self.leftpresstime = variables.settings.current_time
            self.xspeed = -s
            self.lastxupdate = t
        if k in variables.settings.rightkeys:
            self.rightpresstime = variables.settings.current_time
            self.lastxupdate = t
            self.xspeed = s
        if k in variables.settings.upkeys:
            self.uppresstime = variables.settings.current_time
            self.yspeed = -s
            self.lastyupdate = t
        if k in variables.settings.downkeys:
            self.downpresstime = variables.settings.current_time
            self.yspeed = s
            self.lastyupdate = t
        self.change_animation()

    def keyrelease(self, k):
        self.move()
        s = variables.playerspeed * variables.scaleoffset
        t = variables.settings.current_time
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

    #moves with collision detection
    def move(self):
        t = variables.settings.current_time
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
        colliderects = m.colliderects
        numofrocks = len(t)

        #checks if the player collides with a rock
        def collisioncheck(arock, x, y):
            if(arock.mask.overlap(self.mask, [int(x-arock.collidex), int(y-arock.collidey)]) == None):
                return False
            else:
                return True

        playermaskrect = self.mask.get_bounding_rects()[0]


        if not self.xspeed == 0:
            #first check for edges of map, this is the left
            if movedxpos < 0 and m.leftbound:
                self.xpos = 0
                iscollisionx = True
            elif movedxpos+self.normal_width>m.finalimage.get_width() and m.rightbound:
                self.xpos = m.finalimage.get_width()-self.normal_width
                iscollisionx = True
            else:
                #collision detection for the moved x pos with the unmoved y pos
                for x in range(0, len(colliderects)):
                    p = self.normal_height/29
                    #make playerR only the feet
                    playerR = Rect(movedxpos+playermaskrect.x, self.ypos+playermaskrect.y,
                                   playermaskrect.w, playermaskrect.h)
                    if(playerR.colliderect(colliderects[x]) == 1):
                        iscollisionx = True
                        break
                for x in range(0, numofrocks):
                    r = t[x]
                    if collisioncheck(r, movedxpos, self.ypos):
                        iscollisionx = True
                        break

        if not self.yspeed == 0:
            if movedypos < 0 and m.topbound:
                self.ypos = 0
                iscollisiony = True
            elif movedypos+self.normal_height>m.finalimage.get_height() and m.bottombound:
                self.ypos = m.finalimage.get_height()-self.normal_height
                iscollisiony = True
            else:
                #collision detection for the moved y pos with the unmoved x pos
                for x in range(0, len(colliderects)):
                    p = self.normal_height/29
                    #make playerR only the feet
                    playerR = Rect(self.xpos+playermaskrect.x, movedypos+playermaskrect.y,
                                   playermaskrect.w, playermaskrect.h)
                    if(playerR.colliderect(colliderects[x]) == 1):
                        iscollisiony = True
                        break
                for x in range(0, numofrocks):
                    r = t[x]
                    if collisioncheck(r, self.xpos, movedypos):
                        iscollisiony = True
                        break

        if not iscollisionx:
            self.xpos = movedxpos

        if not iscollisiony:
            self.ypos = movedypos

        self.lastxupdate = variables.settings.current_time
        self.lastyupdate = variables.settings.current_time


    def current_pic_scaled(self): # returns the current pic to display
        if self.leftpresstime == 0 and self.rightpresstime == 0 and \
            self.uppresstime == 0 and self.downpresstime == 0:
            c = self.current_animation.pics[0]
        else:
            c = self.current_animation.current_frame()
        c = pygame.transform.scale(c["img"],
                                    [int(c["w"]*variables.scaleoffset),
                                     int(c["h"]*variables.scaleoffset)])
        self.current_display = c

    def scale_by_offset(self):
        c = self.right_animation.pics[1]
        maskpic = pygame.transform.scale(c["img"],
                                    [int(c["w"]*variables.scaleoffset),
                                     int(c["h"]*variables.scaleoffset)])
        #this is to chop off the collision box for only the bottom of honey
        maskpic.fill(pygame.Color(0,0,0,0), [0, 0, maskpic.get_width(), maskpic.get_height()*(26/29)])
        self.mask = pygame.mask.from_surface(maskpic)
        self.normal_width = maskpic.get_width()
        self.normal_height = maskpic.get_height()
        s = variables.playerspeed * variables.scaleoffset
        if(self.xspeed>0):
            self.xspeed = s
        if(self.xspeed<0):
            self.xspeed = -s
        if(self.yspeed<0):
            self.yspeed = -s
        if(self.yspeed>0):
            self.yspeed = s

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

    def soft_change_of_state(self):
        self.lastxupdate = variables.settings.current_time
        self.lastyupdate = variables.settings.current_time
