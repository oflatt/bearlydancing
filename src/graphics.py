#!/usr/bin/python

import pygame, os, variables, rdrawtree, rdrawland, rdrawrock
from datetime import date

today = date.today()
christmasp = False
if today.month == 12:
    christmasp = True

viewfactor = variables.unrounded_displayscale
viewfactorrounded = variables.displayscale

def sscale(img, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = viewfactorrounded
    else:
        endsize = viewfactor
    return pygame.transform.scale(img, [int(w*endsize), int(h*endsize)])

#like sscale but instead of returning a scaled pic, it returns what the dimensions of the new pic would have been
def sscale_dimensions(img, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = viewfactorrounded
    else:
        endsize = viewfactor
    return [int(w*endsize), int(h*endsize)]

def sscale_customfactor(img, factor, rounded = True):
    w = img.get_width()
    h = img.get_height()
    if rounded:
        endsize = viewfactorrounded
    else:
        endsize = viewfactor
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
    return pygame.image.load(os.path.join('pics', filename)).convert_alpha()

#simport returns a dictionary with an image and what its new dimensions would be if scaled
def simport(filename):
    p = importpic(filename)
    dimensions = [p.get_width(), p.get_height()]
    return {"img":p, "w":dimensions[0], "h":dimensions[1]}

# some text used for battles
feedback_factor = 0.75
Atext = sscale_customfactor(variables.font.render("A", 0, variables.WHITE).convert(), feedback_factor)
Stext = sscale_customfactor(variables.font.render("S", 0, variables.WHITE).convert(), feedback_factor)
Dtext = sscale_customfactor(variables.font.render("D", 0, variables.WHITE).convert(), feedback_factor)
Ftext = sscale_customfactor(variables.font.render("F", 0, variables.WHITE).convert(), feedback_factor)
Jtext = sscale_customfactor(variables.font.render("J", 0, variables.WHITE).convert(), feedback_factor)
Ktext = sscale_customfactor(variables.font.render("K", 0, variables.WHITE).convert(), feedback_factor)
Ltext = sscale_customfactor(variables.font.render("L", 0, variables.WHITE).convert(), feedback_factor)
SEMICOLONtext = sscale_customfactor(variables.font.render(";", 0, variables.WHITE).convert(), feedback_factor)
PERFECTtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("PERFECT", 0, variables.WHITE).convert(), feedback_factor), -45)
OKtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("OK", 0, variables.WHITE).convert(), feedback_factor), -45)
GOODtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("GOOD", 0, variables.WHITE).convert(), feedback_factor), -45)
MISStext = pygame.transform.rotate(sscale_customfactor(variables.font.render("MISS", 0, variables.WHITE).convert(), feedback_factor), -45)

# GR is the master dictionary of all image assets
GR = {}
# TextGR is a dictionary of dictionaries for scaled text images and also has another dictionary layer for color
TextGR = {}
# SGR is a dictionary of dictionaries. The inner dictionaries contain scales as the keys and images as the values
# the purpose of SGR is to keep a list of all the scaled pictures for use
SGR = {}
# an SGR for masks
MGR = {}

picnames = os.listdir(os.path.dirname(os.path.abspath("__file__")) + "/pics")

def nicename(filename):
    return filename.replace(".png", "").lower()

def addtoGR(filename):
    p = simport(filename)
    GR[nicename(filename)] = p

def addsurfaceGR(s, name, dimensions = None):
    if dimensions == None:
        dimensions = [s.get_width(), s.get_height()]
    GR[name] = {"img":s,"w":dimensions[0],"h":dimensions[1]}

def getTextPic(text, textheight, color = variables.BLACK):
    if not text in TextGR:
        TextGR[text] = {}
    if not textheight in TextGR[text]:
        TextGR[text][textheight] = {}
    if not color in TextGR[text][textheight]:
        TextGR[text][textheight][color] = scale_pure(variables.font.render(text, 0, color).convert(), textheight, "height")
        
    return TextGR[text][textheight][color]

for x in picnames:
    addtoGR(x)

# down arrow used for conversations
DOWNARROW = pygame.Surface([5, 8], pygame.SRCALPHA)
pygame.draw.polygon(DOWNARROW, variables.WHITE, [[0, 4], [4, 4], [2, 7]])
DOWNARROW.fill(variables.WHITE, pygame.Rect(1, 0, 3, 3))
RIGHTARROW = pygame.transform.rotate(DOWNARROW, 90)
addsurfaceGR(DOWNARROW, "downarrow")
addsurfaceGR(RIGHTARROW, "rightarrow")


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


def endofgeneration():
    variables.draw_progress_bar()
    
def pinetree():
    variables.pinetreesused += 1
    filename = "randompinetree" + str(variables.pinetreesused-1) + ".png"

    if not os.path.exists("pics/" + filename):
        pygame.image.save(rdrawtree.maketree(), "pics/" + filename)
        addtoGR(filename)
    elif variables.newworldeachloadq:
        os.remove(os.path.dirname(os.path.abspath("__file__")) + "/pics/" + filename)
        pygame.image.save(rdrawtree.maketree(), "pics/" + filename)
        addtoGR(filename)
    nicetreename = nicename(filename)

    # christmas!
    if christmasp:
        rdrawtree.makechristmastree(GR[nicetreename]["img"])
    
    endofgeneration()
    return nicetreename

def greyrock():
    variables.greyrocksused += 1
    filename = "randomgreyrock" + str(variables.greyrocksused-1) + ".png"

    if not os.path.exists("pics/" + filename):
        pygame.image.save(rdrawrock.makerock(), "pics/" + filename)
        addtoGR(filename)
    elif variables.newworldeachloadq:
        os.remove(os.path.dirname(os.path.abspath("__file__")) + "/pics/" + filename)
        pygame.image.save(rdrawrock.makerock(), "pics/" + filename)
        addtoGR(filename)

    endofgeneration()
    return nicename(filename)

def grassland(width, height, leftpath = True, rightpath = True, uppath = False, downpath = False):
    variables.grasslandsused += 1
    filename = "randomgrassland" + str(variables.grasslandsused-1) + ".png"

    newland = rdrawland.makegrassland(width, height, leftpath, rightpath, uppath, downpath)
    
    if not os.path.exists("pics/" + filename):
        pygame.image.save(newland, "pics/" + filename)
        addtoGR(filename)
    elif variables.newworldeachloadq:
        os.remove(os.path.dirname(os.path.abspath("__file__")) + "/pics/" + filename)
        pygame.image.save(newland, "pics/" + filename)
        addtoGR(filename)

    endofgeneration()
    return nicename(filename)
