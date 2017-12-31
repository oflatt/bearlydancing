#!/usr/bin/python
import pygame, variables, maps, stathandeling
from graphics import GR, getpic, addmask, getmask
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
    left_animation = Animation(["honeyside3", "honeyside4", "honeyside3", "honeyside4"], 200)
    right_animation = Animation(["honeyside0", "honeyside1",
                                 "honeyside0", "honeyside2"], 200)
    down_animation = Animation(["honeyback3", "honeyback4",
                                "honeyback3", "honeyback5"], 200)
    up_animation = Animation(["honeyback0", "honeyback1",
                              "honeyback0", "honeyback2"], 200)
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
        w = m.map_width
        h = m.map_height
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

    def collisioncheck(self,xpos, ypos):
        cmask = getmask("playermask", variables.scaleoffset)
        #checks if the player collides with a rock
        def rockcollisioncheck(arock, x, y):
            rockmask = arock.get_mask()
            if(rockmask.overlap(cmask, [int(x-arock.collidex), int(y-arock.collidey)]) == None):
                return False
            else:
                return True
        
        iscollision = False

        playermaskrect = cmask.get_bounding_rects()[0]
        m = maps.current_map
        t = m.terrain
        colliderects = m.colliderects
        numofrocks = len(t)
        
        #first check for edges of map, this is the left
        if xpos < 0 and m.leftbound:
            iscollision = True
        elif xpos+self.normal_width>m.map_width and m.rightbound:
            iscollision = True
        elif ypos < 0 and m.topbound:
            iscollision = True
        elif ypos+self.normal_height>m.map_height and m.bottombound:
            iscollision = True
        else:
            #collision detection for the moved x pos with the unmoved y pos
            for x in range(0, len(colliderects)):
                p = self.normal_height/29
                #make playerR only the feet
                playerR = Rect(xpos+playermaskrect.x, ypos+playermaskrect.y,
                               playermaskrect.w, playermaskrect.h)
                if(playerR.colliderect(colliderects[x]) == 1):
                    iscollision = True
                    break
            if not iscollision:
                for x in range(0, numofrocks):
                    r = t[x]
                    if rockcollisioncheck(r, xpos, ypos):
                        iscollision = True
                        break
        return iscollision
    
    #moves with collision detection
    def move(self):
        # save old for use in going back if collide in new map
        self.oldxpos = self.xpos
        self.oldypos = self.ypos
        
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


        if not self.xspeed == 0:
            iscollisionx = self.collisioncheck(movedxpos, self.ypos)
            
        if not self.yspeed == 0:
            iscollisiony = self.collisioncheck(self.xpos, movedypos)

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
        
        self.current_display = getpic(c, variables.scaleoffset)

    def scale_by_offset(self):
        c = self.right_animation.pics[1]
        maskpic = getpic(c, variables.scaleoffset).copy()
        
        #this is to chop off the collision box for only the bottom of honey
        maskpic.fill(pygame.Color(0,0,0,0), [0, 0, maskpic.get_width(), maskpic.get_height()*(26/29)])
        addmask(pygame.mask.from_surface(maskpic), "playermask", variables.scaleoffset)
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
