#!/usr/bin/python
import pygame, variables, stathandeling, math, play_sound, devoptions
from variables import sign
from random import randint
from random import uniform
from graphics import GR, getpic, getmask, getshadow
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
        self.olddrawx = None
        self.olddrawy = None
        self.mapdrawx = 0
        self.oldmapdrawx = 0
        self.mapdrawy = 0
        self.oldmapdrawy = 0
        self.oldsnowpos = (None, None)
        
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

        if devoptions.args.novideomode:
            self.normal_width = 20
            self.normal_height = 30
        else:
            self.normal_width = GR[self.right_animation.pics[1]]["w"]
            self.normal_height = GR[self.right_animation.pics[1]]["h"]
        self.collidesection = (0, self.normal_height * (26/29), self.normal_width, self.normal_height/2)
        self.exp = stathandeling.lvexp(1)
        self.health = stathandeling.max_health(1)

        # a list of all the scales the player has
        self.scales = ["major"]

        # a list of all the soundpacks the player has
        self.soundpacks = ["sine"]

        # a dictionary mapping events (strings) to the number of times it has happened
        self.storyevents = {}

        # a list of points for snow clumps
        # snow clumps are a tuple with x, y, then radius
        self.feetsnowclumps = []
        
        self._freeze()

    def lv(self):
        return stathandeling.explv(self.exp)
        

    def teleport(self, x, y):
        if not x == "same":
            self.xpos = x
        if not y == "same":
            self.ypos = y

    def snowclumpradius(self):
        return int(self.normal_width*variables.compscale()*0.25)

    # drawpos handles the positions for view- this means scaling the coordinates up by compscale
    def update_drawpos(self, current_map):
        self.oldmapdrawx = self.mapdrawx
        self.oldmapdrawy = self.mapdrawy
        self.olddrawx = self.drawx
        self.olddrawy = self.drawy
        
        x = self.xpos * variables.compscale()
        y = self.ypos * variables.compscale()
        
        w = current_map.map_width() * variables.compscale()
        h = current_map.map_height() * variables.compscale()
        
        pwidth = self.normal_width * variables.compscale()
        pheight = self.normal_height * variables.compscale()
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
        self.drawx += current_map.screenxoffset()
        self.mapdrawx -= current_map.screenxoffset()

        #round to nearest pixel
        self.mapdrawx = int(self.mapdrawx)
        self.mapdrawy = int(self.mapdrawy)

    def drawsnowtrail(self, current_map):
        
        background = getpic(current_map.finalimage, variables.compscale())
        feetw = self.collidesection[2]*variables.compscale()
        pathradius = feetw*0.3
        footoffsetx = self.collidesection[0]*variables.compscale()+feetw/2
        footoffsety = self.collidesection[1]*variables.compscale()
        
        standingpos = (int(self.xpos*variables.compscale()+footoffsetx), int(self.ypos*variables.compscale()+footoffsety))
        forwardpos = (int(self.xpos*variables.compscale()+footoffsetx+sign(self.xspeed)*pathradius), int(self.ypos*variables.compscale()+footoffsety+sign(self.yspeed)*pathradius))
        
        standingcolor = background.get_at(standingpos)
        
        if forwardpos[0]>=background.get_width() or forwardpos[0] < 0 or forwardpos[1]>=background.get_height() or forwardpos[1]<0:
            forwardcolor = (1,2,3)
        else:
            forwardcolor = background.get_at(forwardpos)

        if standingcolor[0] == standingcolor[1] == standingcolor[2] and forwardcolor[0] == forwardcolor[1] == forwardcolor[2]:
            greysnow = (variables.snowcolor[0]-10, variables.snowcolor[1]-10, variables.snowcolor[2]-10)
            newdrawcomp = (int(self.drawx+self.mapdrawx+footoffsetx), int(self.drawy+self.mapdrawy+footoffsety))

            if self.oldsnowpos == (None, None):
                self.oldsnowpos = newdrawcomp


            particlebandwidth = pathradius/4.5

            # draw a particle
            def randsnowparticle(xpos, ypos):
                angle = uniform(0, 2*math.pi)
                mag = uniform(pathradius - particlebandwidth/2, pathradius + particlebandwidth/2)
                rgrey = randint(160, 245)
                dotx = xpos + math.cos(angle)*mag-variables.compscale()/2
                doty = ypos + math.sin(angle)*mag-variables.compscale()/2

                pygame.draw.rect(background, (rgrey, rgrey, rgrey),  Rect(dotx, doty, variables.compscale(), variables.compscale()))



            # draw the particles on the circle
            for x in range(10):
                randsnowparticle(newdrawcomp[0], newdrawcomp[1])

            # draw a line for the ditch over circle and particles
            linestart = self.oldsnowpos
            lineend = newdrawcomp
            linewidth = pathradius*2-particlebandwidth*2

            # draw a little circle to smooth edges
            pygame.draw.circle(background, greysnow, lineend, int(linewidth/2))
            pygame.draw.circle(background, greysnow, linestart, int(linewidth/2))


            leftb = (self.xpos+self.collidesection[0])*variables.compscale()
            rightb = leftb + feetw
            topb = (self.ypos + self.collidesection[1]+self.collidesection[3]/2)*variables.compscale() - feetw/3
            bottomb = ((self.ypos + self.collidesection[1]+self.collidesection[3]/2)*variables.compscale()) + feetw/20
            # snow clumps at feet
            i = 0
            xchange = self.xpos - self.oldxpos
            ychange = self.ypos-self.oldypos
            while(i<len(self.feetsnowclumps)):
                p = self.feetsnowclumps[i]
                if p[2] < self.snowclumpradius():
                    self.feetsnowclumps[i] = (p[0]+ xchange*variables.compscale(), p[1]+ychange*variables.compscale(), p[2]+self.snowclumpradius()/500)

                if p[0]<leftb or p[0]>rightb or p[1]<topb or p[1]>bottomb:
                    del self.feetsnowclumps[i]
                    i-=1

                i+=1

            if(len(self.feetsnowclumps) < 7):
                if uniform(0, 110)>93+len(self.feetsnowclumps):
                    self.feetsnowclumps.append((randint(int(leftb), int(rightb)), randint(int(topb), int(bottomb)), uniform(self.snowclumpradius()/2, self.snowclumpradius())))


            # set the old snow pos to current pos
            self.oldsnowpos = newdrawcomp
        else:
            self.feetsnowclumps = []
        
    def draw(self, current_map):
        mapbasename = current_map.finalimage
        snowp = mapbasename[0:14] == "randomsnowland"

        if current_map.shadowsp:
            shadow = self.current_shadow()
            variables.screen.blit(shadow.surface, [self.drawx + shadow.xoffset, self.drawy + shadow.yoffset])
        
        
        variables.screen.blit(self.current_pic_scaled(), [self.drawx, self.drawy])
        
        
        if self.mapdrawx != self.oldmapdrawx or self.mapdrawy != self.oldmapdrawy:
            variables.dirtyrects = [Rect(0,0,variables.width, variables.height)]
        else:
            if snowp:
                # bigger dirtyrect for the snow balls
                bearrect = Rect(self.drawx - self.snowclumpradius()*1.5,
                                                 self.drawy-variables.compscale()*5,
                                                 self.normal_width*variables.compscale()+self.snowclumpradius()*3,
                                                 self.normal_height*variables.compscale() + self.snowclumpradius()*3+variables.compscale()*5)
            else:
                bearrect = Rect(self.drawx-variables.compscale()*3, self.drawy-variables.compscale()*3, self.normal_width*variables.compscale()+6*variables.compscale(), self.normal_height*variables.compscale() + 6 * variables.compscale())

            if current_map.shadowsp:
                shadowrect = Rect(self.drawx+shadow.xoffset, self.drawy+shadow.yoffset, shadow.surface.get_width()+variables.compscale()*3, shadow.surface.get_height()+variables.compscale() *3)
            
                variables.dirtyrects.append(variables.combinerects(shadowrect, bearrect))
            else:
                variables.dirtyrects.append(bearrect)

        # for snow draw trail
        if snowp:
            if not self.olddrawx == None and self.ismoving():
                self.drawsnowtrail(current_map)

            
            # now draw snow clumps on bear
            for p in self.feetsnowclumps:
                pygame.draw.circle(variables.screen, (variables.snowcolor[0] + 10, variables.snowcolor[1]+10, variables.snowcolor[2]+10), (int(p[0])-self.mapdrawx, int(p[1])-self.mapdrawy), int(p[2]))

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
            self.lastxupdate = t-16
        if variables.checkkey("right", k):
            self.rightpresstime = variables.settings.current_time
            self.lastxupdate = t-16
            self.xspeed = s
        if variables.checkkey("up", k):
            self.uppresstime = variables.settings.current_time
            self.yspeed = -s
            self.lastyupdate = t-16
        if variables.checkkey("down", k):
            self.downpresstime = variables.settings.current_time
            self.yspeed = s
            self.lastyupdate = t-16
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

    def collisioncheck(self, xpos, ypos, current_map):
        cmask = getmask(self.right_animation.pics[1], self.collidesection)
        #checks if the player collides with a rock
        def rockcollisioncheck(arock, x, y):
            rockmask = arock.get_mask()
            if(rockmask.overlap(cmask, [int(x-arock.x), int(y-arock.y)]) == None):
                return False
            else:
                return True
        
        iscollision = False

        playermaskrect = cmask.get_bounding_rects()[0]
        m = current_map
        t = m.terrain
        colliderects = m.colliderects
        numofrocks = len(t)
        
        #first check for edges of map, this is the left
        if xpos < 0 and m.leftbound:
            iscollision = True
        elif xpos+self.normal_width>m.map_width() and m.rightbound:
            iscollision = True
        elif ypos < 0 and m.topbound:
            iscollision = True
        elif ypos+self.normal_height>m.map_height() and m.bottombound:
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
    def move(self, current_map):
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
        m = current_map


        if not self.xspeed == 0:
            iscollisionx = self.collisioncheck(movedxpos, self.ypos, current_map)
            
        if not self.yspeed == 0:
            iscollisiony = self.collisioncheck(self.xpos, movedypos, current_map)

        if not iscollisionx:
            self.xpos = movedxpos

        if not iscollisiony:
            self.ypos = movedypos

        self.lastxupdate = variables.settings.current_time
        self.lastyupdate = variables.settings.current_time

    def current_pic_name(self):
        if self.leftpresstime == 0 and self.rightpresstime == 0 and \
            self.uppresstime == 0 and self.downpresstime == 0:
            c = self.current_animation.pics[0]
        else:
            c = self.current_animation.current_frame()
        return c

    def current_pic_scaled(self): # returns the current pic to display
        return getpic(self.current_pic_name(), variables.compscale())

    def current_shadow(self):
        return getshadow(self.current_pic_name(), variables.compscale())

    def new_scale_offset(self):
        # stop a streak from happening with path in snow
        self.olddrawx = None
        self.olddrawy = None
        self.drawx = None
        self.drawy = None
        self.oldsnowpos = (None, None)
        
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

    def addreward(self, reward):
        if reward in play_sound.scales:
            if not reward in self.scales:
                self.scales.append(reward)
        elif reward in play_sound.soundpackkeys:
            if not reward in self.soundpacks:
                self.soundpacks.append(reward)
