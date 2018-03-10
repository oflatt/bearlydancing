#!/usr/bin/python
import pygame, variables, maps, stathandeling
from graphics import GR, getpic, getmask
from Animation import Animation
from pygame import Rect
from FrozenClass import FrozenClass

class Player(FrozenClass):

    def __init__(self):
        self.xspeed = 0
        self.yspeed = 0
        self.leftpresstime = 0
        self.rightpresstime = 0
        self.uppresstime = 0
        self.downpresstime = 0
        self.xpos = 0
        self.oldxpos = 0
        self.ypos = 0
        self.oldypos = 0
        self.drawx = 0
        self.drawy = 0
        self.mapdrawx = 0
        self.oldmapdrawx = 0
        self.mapdrawy = 0
        self.oldmapdrawy = 0
        self.lastxupdate = 0
        self.lastyupdate = 0
        self.timeslost = 0
        self.totalbattles = 0

        #animation
        self.left_animation = Animation(["honeyside3", "honeyside4", "honeyside3", "honeyside4"], 200)
        self.right_animation = Animation(["honeyside0", "honeyside1",
                                     "honeyside0", "honeyside2"], 200)
        self.down_animation = Animation(["honeyback3", "honeyback4",
                                    "honeyback3", "honeyback5"], 200)
        self.up_animation = Animation(["honeyback0", "honeyback1",
                                  "honeyback0", "honeyback2"], 200)
        self.current_animation = self.right_animation

        self.normal_width = GR[self.right_animation.pics[1]]["w"]
        self.normal_height = GR[self.right_animation.pics[1]]["h"]
        self.collidesection = (0, self.normal_height * (26/29), self.normal_width, self.normal_height/2)
        self.exp = 0
        self.health = stathandeling.max_health(1)

        # a list of all the scales the player has
        self.scales = ["C major"]

        # a dictionary mapping events (strings) to the number of times it has happened
        self.storyevents = {}
        
        self._freeze()

    def lv(self):
        return stathandeling.explv(self.exp)
        

    def teleport(self, x, y):
        if not x == "same":
            self.xpos = x
        if not y == "same":
            self.ypos = y

    def update_drawpos(self):
        self.oldmapdrawx = self.mapdrawx
        self.oldmapdrawy = self.mapdrawy
        x = self.xpos * variables.compscale
        y = self.ypos * variables.compscale
        m = maps.current_map
        w = m.map_width * variables.compscale
        h = m.map_height * variables.compscale
        
        pwidth = self.normal_width * variables.compscale
        pheight = self.normal_height * variables.compscale
        hpheight = pheight/2
        hpwidth = pwidth/2
        screenhw = variables.width/2
        screenhh = variables.height/2
        
        if w <= variables.width:
            # if the map fits in the screen, no scrolling needed
            self.drawx = x
            self.mapdrawx = 0
        elif x < screenhw - hpwidth:  # if it is in the left side of the map
            self.mapdrawx = 0  # do not scroll the map at all
            self.drawx = x
        elif x > (w - screenhw - hpwidth):  # if it is on the right side of the map
            self.mapdrawx = w - variables.width  # set it to the maximum scroll
            self.drawx = x - (w-variables.width)
        else:
            # otherwise, scroll it by pos (accounting for the initial non-scolling area)
            self.mapdrawx = x - screenhw + hpwidth
            self.drawx = screenhw - hpwidth

        if h <= variables.height:
            self.drawy = y
            self.mapdrawy = 0
        elif y < screenhh - hpheight:  # same but for y pos
            self.mapdrawy = 0
            self.drawy = y
        elif y > (h - screenhh - hpheight):
            self.mapdrawy = h - variables.height
            self.drawy = y - (h-variables.height)
        else:
            self.mapdrawy = y - screenhh + hpheight
            self.drawy = screenhh - hpheight

        # then add the map's x offset for drawing small maps in the middle
        self.drawx += m.screenxoffset
        self.mapdrawx -= m.screenxoffset

        #round to nearest pixel
        self.mapdrawx = int(self.mapdrawx)
        self.mapdrawy = int(self.mapdrawy)

    def draw(self):
        variables.screen.blit(self.current_pic_scaled(), [self.drawx, self.drawy])
        if self.mapdrawx != self.oldmapdrawx or self.mapdrawy != self.oldmapdrawy:
            variables.dirtyrects = [Rect(0,0,variables.width, variables.height)]
        else:
            variables.dirtyrects.append(Rect(self.drawx-variables.compscale*3, self.drawy-variables.compscale*3, self.normal_width*variables.compscale+6*variables.compscale, self.normal_height*variables.compscale + 6 * variables.compscale))

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
        s = variables.playerspeed
        if variables.checkkey("left", k):
            self.leftpresstime = variables.settings.current_time
            self.xspeed = -s
            self.lastxupdate = t
        if variables.checkkey("right", k):
            self.rightpresstime = variables.settings.current_time
            self.lastxupdate = t
            self.xspeed = s
        if variables.checkkey("up", k):
            self.uppresstime = variables.settings.current_time
            self.yspeed = -s
            self.lastyupdate = t
        if variables.checkkey("down", k):
            self.downpresstime = variables.settings.current_time
            self.yspeed = s
            self.lastyupdate = t
        self.change_animation()

    def keyrelease(self, k):
        s = variables.playerspeed
        t = variables.settings.current_time
        if variables.checkkey("left", k):
            self.leftpresstime = 0
            self.lastxupdate = t
            if self.rightpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = s
        elif variables.checkkey("right", k):
            self.rightpresstime = 0
            self.lastxupdate = t
            if self.leftpresstime == 0:
                self.xspeed = 0
            else:
                self.xspeed = -s
        elif variables.checkkey("up", k):
            self.lastyupdate = t
            self.uppresstime = 0
            if self.downpresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = s
        elif variables.checkkey("down", k):
            self.lastyupdate = t
            self.downpresstime = 0
            if self.uppresstime == 0:
                self.yspeed = 0
            else:
                self.yspeed = -s
        self.change_animation()

    def collisioncheck(self, xpos, ypos):
        cmask = getmask(self.right_animation.pics[1], self.collidesection)
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
            #make playerR only the feet
            playerR = Rect(xpos+playermaskrect.x, ypos+playermaskrect.y,
                           playermaskrect.w, playermaskrect.h)
            
            #collision detection for the moved x pos with the unmoved y pos
            for x in range(0, len(colliderects)):
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
        
        return getpic(c, variables.compscale)

    def new_scale_offset(self):
        pass

        
    def ismoving(self):
        return not (self.xspeed==0 and self.yspeed==0)

    def heal(self):
        self.health = stathandeling.max_health(self.lv())

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

    def addstoryevents(self, events):
        if events != None:
            for e in events:
                self.addstoryevent(e)
        
    def addstoryevent(self, event):
        if event != None:
            if event in self.storyevents:
                self.storyevents[event] += 1
            else:
                self.storyevents[event] = 1

    # returns number of times that event has occured
    def getstoryevent(self, event):
        if event in self.storyevents:
            return self.storyevents[event]
        else:
            return 0
