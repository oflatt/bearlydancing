#!/usr/bin/python

import pygame, os, variables, random, datetime
from pygame import Rect
import string, math

from rdraw.rdrawrock import makerock
from rdraw.rdrawtree import maketree, makechristmastree
from rdraw.rdrawland import makegrassland, makesnowland
from rdraw.rdrawmodify import createshadow
from rdraw.rdrawflower import makeflower
from rdraw.rdrawarcade import makecabinet
from Shadow import Shadow
import special_graphics_loader

today = datetime.date.today()
christmasp = False
if today.month == 12:
    christmasp = True

def sscale(img, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = variables.displayscale
    else:
        endsize = variables.unrounded_displayscale
    return pygame.transform.scale(img, [int(w*endsize), int(h*endsize)])

#like sscale but instead of returning a scaled pic, it returns what the dimensions of the new pic would have been
def sscale_dimensions(img, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = variables.displayscale
    else:
        endsize = variables.unrounded_displayscale
    return [int(w*endsize), int(h*endsize)]

def sscale_customfactor(img, factor, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = variables.displayscale
    else:
        endsize = variables.unrounded_displayscale
    return pygame.transform.scale(img, [int(w*endsize*factor), int(h*endsize*factor)])

#use if you want pictures where the smaller dimension is a set size
def scale_pure(img, s, side = None):
    w = img.get_width()
    h = img.get_height()
    if side == "w" or side == "width":
        smaller = w
    elif side == "h" or side == "height":
        smaller = h
    elif w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller) * s), int((h/smaller) * s)])

def importpic(filename):
    
    pic = pygame.image.load(os.path.join(variables.pathtoself, os.path.join('pics', filename)))
    # a list of types of pictures with no alpha in them
    backgrounds = ["randomgrassland", "randomsnowland"]
    
    if typename(filename) in backgrounds:
        return pic.convert()
    else:
        return pic.convert_alpha()

#simport returns a dictionary with an image and what its new dimensions would be if scaled
def simport(filename):
    p = importpic(filename)
    dimensions = [p.get_width(), p.get_height()]
    return {"img":p, "w":dimensions[0], "h":dimensions[1]}


# GR is the master dictionary of all image assets
GR = {}
# TextGR is a dictionary of dictionaries for scaled text images and also has another dictionary layer for color
TextGR = {}
# SGR is a dictionary of dictionaries. The inner dictionaries contain scales as the keys and images as the values
# the purpose of SGR is to keep a list of all the scaled pictures for use
SGR = {}
# an SGR for masks
MGR = {}
# an SGR for shadows
shadowGR = {}

picnames = os.listdir(variables.pathtoself + "/pics")

def nicename(filename):
    return filename.replace(".png", "").lower()

def typename(filename):
    return nicename(filename).rstrip(string.digits)

def addtoGR(filename):
    p = simport(filename)
    GR[nicename(filename)] = p

def addsurfaceGR(s, name, dimensions = None):
    special_graphics_loader.addsurfaceGR(GR, s, name, dimensions)
    
# renders text so that the linesize is what matters
def rendertext(text, color, textheight):
    return scale_pure(variables.font.render(text, 0, color).convert(), textheight, "height")
    
def getTextPic(text, textheight, color = variables.BLACK, savep = True):
    if not savep:
        return rendertext(text, color, textheight)
    
    if not text in TextGR:
        TextGR[text] = {}
    if not textheight in TextGR[text]:
        TextGR[text][textheight] = {}
    if not color in TextGR[text][textheight]:
        TextGR[text][textheight][color] = rendertext(text, color, textheight)
        
    return TextGR[text][textheight][color]

# add all the pics in the pic folder
for x in picnames:
    if x != "" and x[0] != ".":
        addtoGR(x)

# load special graphics
special_graphics_loader.load_special_graphics(GR)
        
# count the number of player animations
numofplayerframes = 0
while "honeydance" + str(numofplayerframes) + "-0" in GR:
    numofplayerframes += 1
numofspecialmoveeffects = 0
while "specialmoveeffect" + str(numofspecialmoveeffects) in GR:
    numofspecialmoveeffects += 1

# down arrow used for conversations
DOWNARROW = pygame.Surface([5, 8], pygame.SRCALPHA)
pygame.draw.polygon(DOWNARROW, variables.WHITE, [[0, 4], [4, 4], [2, 7]])
DOWNARROW.fill(variables.WHITE, pygame.Rect(1, 0, 3, 3))
RIGHTARROW = pygame.transform.rotate(DOWNARROW, 90)
addsurfaceGR(DOWNARROW, "downarrow")
addsurfaceGR(RIGHTARROW, "rightarrow")


# for the color of difficulty and combos
# input is a number 0 to 1, where 1 corresponds to the max
def difficultytocolor(colorfactor):
    maxnum = 20
    colorfactor = colorfactor*maxnum
    typecolor = None
    if colorfactor < 1:
        typecolor = (0, 255, 0)
    elif colorfactor < 2:
        typecolor = (150, 255, 0)
    elif colorfactor < 3:
        typecolor = (255, 255, 0)
    elif colorfactor < 8:
        typecolor = (255, 255-(colorfactor - 2)*42, 0)
    elif colorfactor < 16:
        typecolor = (255, 0, 28*(colorfactor-7))
    else:
        typecolor = (255,min((colorfactor-15)*25, 255), 255)
    return typecolor

# processes images before they are cached- currently does nothing
def finalprocessimage(image):
    return image

# this function returns a surface. If no scale is provided, it takes from GR.
# if a scale is provided, it takes the scaled picture from SGR or scales the picture, adds it to SGR, and returns the pic
# scale is multiplied by the displayscale by default, this means for rocks scale is the map scale
def getpic(picname, scale = None):
    if scale == None:
        return GR[picname]["img"]
    else:
        picexistsp = picname in SGR
        if picexistsp and scale in SGR[picname]:
            return SGR[picname][scale]
        else:
            scaledimage = GR[picname]
            scaledimage = pygame.transform.scale(scaledimage["img"], [int(scaledimage["w"]*scale), int(scaledimage["h"]*scale)])
            scaledimage = finalprocessimage(scaledimage)
            if picexistsp:
                SGR[picname][scale] = scaledimage
            else:
                SGR[picname] = {}
                SGR[picname][scale] = scaledimage
            return scaledimage

        
def getpicbyheight(picname, height):
    scale = height/GR[picname]["h"]
    return getpic(picname, scale)

def getpicbywidth(picname, width):                 
    scale = width/GR[picname]["w"]
    return getpic(picname, scale)

# stores unscaled shadows in GR
def getshadowunscaled(picname, shadowangle):
    sname = picname + "shadow"
    picexistsp = sname in GR
    if picexistsp:
        return GR[sname]
    else:
        shadowpic = createshadow(getpic(picname), shadowangle)
        GR[sname] = shadowpic
        return shadowpic

shadowstarthour = 7.5
shadowendhour = 9.5+12
    
# like getpic, but pass in the name of a pic to get the shadow of
# returns a Shadow object
def getshadow(picname, scale = None):
    now = datetime.datetime.now()
    timeminutes = now.hour * 60 + now.minute - shadowstarthour * 60
    
    if timeminutes < 0:
        timeminutes = 0
    elif timeminutes > (shadowendhour-shadowstarthour) * 60:
        timeminutes = (shadowendhour-shadowstarthour) * 60
    # round down to nearest 10 minutes
    timeminutes = int(timeminutes / 10)
    proportionofday = timeminutes / int((shadowendhour-shadowstarthour)*60/10)

    shadowangle = -math.pi/2 + math.pi * proportionofday * 0.8 + math.pi * 0.1
    
    sunscaled = getshadowunscaled(picname, shadowangle)
    sname = picname + str(int(shadowangle*100)/100)
    picexistsp = sname in shadowGR
    if picexistsp and scale in shadowGR[sname]:
        return shadowGR[sname][scale]
    else:
        shadowpic = pygame.transform.scale(sunscaled.surface, (int(scale*sunscaled.surface.get_width()), int(scale*sunscaled.surface.get_height())))
        shadowpic = finalprocessimage(shadowpic)
        shadow = Shadow(shadowpic, sunscaled.xoffset*scale, sunscaled.yoffset*scale)
        if picexistsp:
            shadowGR[sname][scale] = shadow
        else:
            shadowGR[sname] = {}
            shadowGR[sname][scale] = shadow
        return shadow

# maskname refers to a pic in GR and collidesection is a tuple x y width height coordinates for where the mask is taken from
def getmask(maskname, collidesection = None):
    if not maskname in MGR:
        MGR[maskname] = {}
    # if we need to make a new mask
    if not collidesection in MGR[maskname]:
        maskpic = getpic(maskname).copy()
        w = maskpic.get_width()
        h = maskpic.get_height()
        cs = collidesection
        if cs != None:
            # fill all but the collide section
            # top
            maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, w, cs[1]])
            # left
            maskpic.fill(pygame.Color(0, 0, 0, 0), [0, 0, cs[0], h])
            # right
            maskpic.fill(pygame.Color(0, 0, 0, 0), [cs[0] + cs[2], 0, w - (cs[0] + cs[2]), h])
            # bottom
            maskpic.fill(pygame.Color(0, 0, 0, 0), [0, cs[1] + cs[3], w, h - (cs[1] + cs[3]) + 1])

        MGR[maskname][collidesection] = pygame.mask.from_surface(maskpic)

    
    return MGR[maskname][collidesection]


def drawthismessage(messagestring):
    extrabuttonwidth = variables.getmenutextxoffset() / 4
    mpic = getTextPic(messagestring, variables.gettextsize(), variables.WHITE)
    mx = variables.width/2-mpic.get_width()/2
    my = variables.height/2+mpic.get_height()*2
    r = Rect(mx-extrabuttonwidth,
             my,
             mpic.get_width()+2*extrabuttonwidth,
             mpic.get_height())
    variables.screen.fill(variables.BLACK, r)
    variables.screen.blit(mpic, [mx, my])

    variables.dirtyrects.append(r)

def endofgeneration():
    variables.draw_progress_bar()

def startofgeneration(nameofgraphic):
    variables.draw_graphic_name(nameofgraphic)
    
max_sample = 2 ** (16 - 1) - 1
def drawwave(loopbuffer, skiplen, wavex, wavey, waveamp, wavelen, color, dirtyrectp = True):
    wavescalar = waveamp*0.8/(max_sample)
    oldpos = (wavex, wavey)
    for waveoffset in range(int(wavelen)):
        loopscale = loopbuffer[int(waveoffset*skiplen)]
        if len(loopbuffer.shape) > 1:
            # when it is a 2d buffer, just use one side
            loopscale = loopscale[0]
        
        variables.screen.fill(variables.BLUE, Rect(int(wavex+waveoffset), int(wavey), variables.displayscale, variables.displayscale))
        newpos = (int(wavex+waveoffset),int(wavey+(loopscale*wavescalar)))
        pygame.draw.line(variables.screen, color, oldpos, newpos)
        oldpos = newpos
        #variables.screen.fill(color, Rect, variables.displayscale, variables.displayscale))

    if dirtyrectp:
        variables.dirtyrects.append(Rect(wavex, wavey-waveamp, waveoffset, waveamp*2))
    

def randombogoface():
    # first clear the scaled pics for bugo
    if "bugo0" in SGR:
        del SGR["bugo0"]
    if "bugo1" in SGR:
        del SGR["bugo1"]
    
    frame1 = GR["bugo0"]["img"]
    frame2 = GR["bugo1"]["img"]
    
    xoffset = 8
    yoffset = 7

    backgroundcolor = frame1.get_at([xoffset-1, yoffset])
    mouthcolor = frame1.get_at([8,5])
    
    smile = pygame.Surface([5, 2], pygame.SRCALPHA)
    smile.fill(backgroundcolor)

    def mirrorset(point):
        smile.set_at(point, mouthcolor)
        smile.set_at((5-1-point[0], point[1]), mouthcolor)

    # check the points besides the middle points
    if random.random() < 1/3:
        mirrorset((0,0))
    if random.random() < 1/3:
        mirrorset((0,1))

    if random.random() < 1/2:
        mirrorset((1, 0))
    if random.random() < 1/2:
        mirrorset((1, 1))

    if random.random() < 1/2:
        smile.set_at((2, 0), mouthcolor)
    if random.random() < 1/2:
        smile.set_at((2, 1), mouthcolor)

    frame1.blit(smile, (xoffset, yoffset))


    
# takes a function that returns a new surface and a filename and returns the newy made surface name
def generategraphic(generatingfunction, graphicname, newworldoverride = False):
    startofgeneration(graphicname)
    
    if not graphicname in variables.generatedgraphicsused:
        variables.generatedgraphicsused[graphicname] = 1
    else:
        variables.generatedgraphicsused[graphicname] += 1
    
    filename = graphicname + str(variables.generatedgraphicsused[graphicname]-1) + ".png"

    if not os.path.exists(variables.pathtoself + "/pics/" + filename):
        pygame.image.save(generatingfunction(), variables.pathtoself + "/pics/" + filename)
        addtoGR(filename)
    elif variables.newworldeachloadq or (newworldoverride and variables.allownewworldoverridep):
        os.remove(variables.pathtoself + "/pics/" + filename)
        pygame.image.save(generatingfunction(), variables.pathtoself + "/pics/" + filename)
        addtoGR(filename)

    endofgeneration()
    return nicename(filename)
    
def pinetree():
    nicetreename = generategraphic(maketree, "randompinetree")

    # christmas!
    if christmasp:
        makechristmastree(GR[nicetreename]["img"])

    return nicetreename

def snowpinetree():
    def makesnowtree():
        return maketree(True)
    nicetreename = generategraphic(makesnowtree, "randomsnowpinetree")

    # christmas!
    if christmasp:
        makechristmastree(GR[nicetreename]["img"])

    return nicetreename

def greyrock():
    return generategraphic(makerock, "randomgreyrock")

def grassland(width, height, leftpath = True, rightpath = True, uppath = False, downpath = False):
    def callgrasslandfunction():
        return makegrassland(width, height, leftpath, rightpath, uppath, downpath)
    
    return generategraphic(callgrasslandfunction, "randomgrassland")

def snowland(width, height, grasstosnowp = False):
    def callsnowland():
        return makesnowland(width, height, grasstosnowp)

    return generategraphic(callsnowland, "randomsnowland")

def flower():
    return generategraphic(makeflower, "randomflower")

def arcadecabinet(gamename):
    def callmakecabinet():
        return makecabinet(gamename)
    return generategraphic(callmakecabinet, "randomarcadecabinet")
