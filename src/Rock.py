#!/usr/bin/python
import pygame, variables, math
from pygame import Rect
from Animation import Animation
from graphics import GR, getpic, getmask, getshadow
from FrozenClass import FrozenClass


class Rock(FrozenClass):

    def __init__(self, base, x, y, collidesection, name = None):

        self.animations = None

        # base can be either an imagename, a list of imagenames, an animation, or a list of animations
        #if it is just a single image, put it in an animation
        self.animationnum = 0
        if type(base) == Animation:
            self.animations = [base]
        elif type(base) == str:
            self.animations = [Animation([base], 1)]
        else:
            #if it's a list of images, wrap them all in animations
            if type(base[0]) == str:
                for i in range(len(base)):
                    base[i] = Animation([base[i]], 1)
            self.animations = base

        self.name = name
        self.loopanimationsp = False

        # these are used for movement animations
        self.x = x
        self.y = y
        self.w = GR[self.animations[0].pics[0]]["w"]
        self.h = GR[self.animations[0].pics[0]]["h"]

        # used to keep track of if it was drawn for backgroundrange
        self.drawnp = False


        # collidesection is a list x y width height all of the arguments are relative to the rock's pos and dimensions
        # width and height of collidesection are multiplied by the width and height of the base
        self.collidesection = collidesection
        if self.collidesection == None:
            self.collidesection = [0, 0, 0, 0]
        else:
            self.collidesection = self.collidesection.copy()
            self.collidesection[0] *= self.w
            self.collidesection[1] *= self.h
            self.collidesection[2] *= self.w
            self.collidesection[3] *= self.h
        for i in range(len(self.collidesection)):
            self.collidesection[i] = int(self.collidesection[i])
        self.collidesection = tuple(self.collidesection)
        self.set_backgroundrange()

        # variables played with for special moving or hiding rocks
        # hiddenp is if the rock should not be displayed
        # yposfunction and xposfunction are functions to call and add to the respective y and x positions
        self.hiddenp = False
        self.yposfunctions = []
        self.xposfunctions = []
        self.lasty = self.y
        self.lastx = self.x
        self.changetime = None
        self.tickstate = 0

        # if we need to add the dirtyrect for the rock to the screen-for changing animation
        self.updatescreenp = False
        self.updatealways = False

        self._freeze()
        

    def nextanimation(self):
        # add dirty rect
        self.updatescreenp = True
        if self.animationnum+1 < len(self.animations) or self.loopanimationsp:
            self.animationnum = (self.animationnum + 1) % len(self.animations)
            self.animations[self.animationnum].reset()
            self.changetime = variables.settings.current_time

        if self.name == "steve":
            self.xposfunctions = [self.makelinearfunction(variables.settings.current_time, -30/1000, lowerlimit = -100)]

    def draw(self, offset = [0,0]):
        self.drawtick()
        drawx = self.x * variables.compscale() + offset[0]
        drawy = self.y * variables.compscale() + offset[1]
        swidth = self.w * variables.compscale()
        sheight = self.h * variables.compscale()

        # only draw if on screen
        if drawx+swidth>0 and drawx<variables.width and drawy<variables.height and drawy+sheight>0:
            p = getpic(self.animations[self.animationnum].current_frame(), variables.compscale())
            shadow = getshadow(self.animations[self.animationnum].current_frame(), variables.compscale())
            shadowp = shadow.surface
            
            
            if self.updatescreenp:
                variables.dirtyrects.append(Rect(drawx, drawy, max(p.get_width(), shadowp.get_width()), p.get_height()))
                self.updatescreenp = False

            shadowy = drawy + sheight - shadowp.get_height()
            shadowx = drawx
            variables.screen.blit(shadowp, [drawx, shadowy])
            variables.screen.blit(p, [drawx, drawy])
            

    # background range is the range of the player's location that it is drawn behind the player
    def set_backgroundrange(self):
        cs = self.collidesection
        h = GR[self.animations[0].pics[0]]["h"]
        if cs == (0, 0, self.w, self.h):
            self.background_range = Rect(0, self.y, 9999999, 9999999)
        elif cs == (0,0,0,0):
            self.background_range = None
        else:
            self.background_range = Rect(0, int(self.y + cs[1] + cs[3] * (1 / 3)), 9999999, 9999999)

    def get_mask(self):
        return getmask(self.animations[0].pics[0], self.collidesection)

    def getrect(self):
        return Rect(self.x, self.y, self.w, self.h)

    def hide(self):
        self.hiddenp = True

    def makegravityfunction(self, starttime, upperlimit = None, lowerlimit = None):
        return self.makeexponentialfunction(starttime, variables.accelpixelpermillisecond, 0, upperlimit, lowerlimit)

    def makelinearfunction(self, starttime, velocity, minimumheightwithgravity = None, limit = None, delay = None, lowerlimit = None):
        if minimumheightwithgravity != None:
            velocity = -math.sqrt(2*variables.accelpixelpermillisecond*minimumheightwithgravity)
        def ffunction():
            dt = variables.settings.current_time - starttime
            pos = velocity*dt
            if delay != None:
                if dt >= delay:
                    pos = velocity*(dt-delay)
                else:
                    pos = 0
            if limit != None:
                if pos>limit:
                    pos = limit
            if lowerlimit != None:
                if pos<lowerlimit:
                    pos = lowerlimit
            return pos

        return ffunction

    def makeexponentialfunction(self, starttime, accel, yoffset = 0, upperlimit = None, lowerlimit = None):
        def gfunction():
            dt = variables.settings.current_time - starttime
            dpos = (accel/2) * (dt**2) + yoffset
            if upperlimit != None:
                dpos = min(dpos, upperlimit)
            if lowerlimit != None:
                dpos = max(dpos, lowerlimit)
            return dpos
        return gfunction

    def unhide(self):
        self.hiddenp = False

        if self.name == "kewlcorn":
            self.yposfunctions = [self.makegravityfunction(variables.settings.current_time, variables.TREEHEIGHT*(3/4)-self.h)]

    def clearfunctions(self):
        self.xposfunctions = []
        self.yposfunctions = []

    # called just before drawing the rock
    # these functions must be safe so that the functions can be erased in saving
    def drawtick(self):
        if self.updatealways:
            self.updatescreenp = True
        if self.name in ["kewlcorn", "chimney", "tp", "steve"]:
            self.y = self.lasty
            self.x = self.lastx
            for f in self.yposfunctions:
                self.y += f()
            for f in self.xposfunctions:
                self.x += f()
            
            self.updatescreenp = True


        # chimney-
        if self.name == "chimney" and self.animationnum>0:
            # keep it not super out of the screen
            if self.y > 1500:
                self.y = 1400
                self.lasty = 1400
            dt = variables.settings.current_time - self.changetime
            
            if self.animationnum == 1:
                if dt >= self.animations[1].framerate*len(self.animations[self.animationnum].pics):
                    self.nextanimation()
                    # also start moving to the right
                    self.xposfunctions = [self.makelinearfunction(variables.settings.current_time,
                                                                  20/1000,
                                                                  limit=450-self.lastx,
                                                                  delay = self.animations[self.animationnum].framerate)]
            elif self.animationnum == 2:
                framerate = self.animations[self.animationnum].framerate
                

                # if we do a flap
                flapp = False

                # devide by 2 because only on downwards flapping
                if ((dt /framerate) - 1) / 2 >= self.tickstate:
                    self.tickstate = int((dt/framerate - 1) / 2) + 1
                    flapp = True
                    
                # if we do a flap- don't do it if above the screen, so it can fall in
                if flapp and self.y > 0:
                    flapstarttime = variables.settings.current_time - variables.settings.current_time%framerate
                    flapheight= max(25, self.y-100)
                    timeoffsetforheight = math.sqrt(flapheight*2/variables.accelpixelpermillisecond)
                    # jump up
                    self.yposfunctions = [self.makeexponentialfunction(flapstarttime+timeoffsetforheight,
                                                                       variables.accelpixelpermillisecond, -flapheight)]

                    # set the pos for reference
                    self.lasty = self.y
                    
        elif self.name == "tp" and self.animationnum>0 and self.y <= 1000:
            dt = variables.settings.current_time - self.changetime
            framerate = self.animations[self.animationnum].framerate
            
            if int(((dt/framerate)+2)/len(self.animations[self.animationnum].pics))-1 >= self.tickstate:
                jumpduration = framerate * 3
                jumpstarttime = variables.settings.current_time - variables.settings.current_time%framerate
                jumpheight = 22
                timeoffsetforheight = math.sqrt(jumpheight*2/variables.accelpixelpermillisecond)
                self.yposfunctions = [self.makeexponentialfunction(jumpstarttime+timeoffsetforheight, variables.accelpixelpermillisecond, -jumpheight, upperlimit = 0)]
                xvel = 55/1000
                self.xposfunctions = [self.makelinearfunction(jumpstarttime, xvel, limit = (xvel*jumpduration))]
                self.lasty = self.y
                self.lastx = self.x
                self.tickstate += 1

                # if since last tick it has been an entire jump, just dissapear
                if dt>jumpduration*2:
                    self.x = 1001
                    self.lastx = 1001
                    self.clearfunctions()
                    

    # currently not used
    def ontick(self):
        pass
    
                
            
