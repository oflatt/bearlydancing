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
    dimensions = sscale_dimensions(p)
    return {"img":p, "w":dimensions[0], "h":dimensions[1]}

feedback_factor = 0.75
Atext = sscale_customfactor(variables.font.render("A", 0, variables.WHITE), feedback_factor)
Stext = sscale_customfactor(variables.font.render("S", 0, variables.WHITE), feedback_factor)
Dtext = sscale_customfactor(variables.font.render("D", 0, variables.WHITE), feedback_factor)
Ftext = sscale_customfactor(variables.font.render("F", 0, variables.WHITE), feedback_factor)
Jtext = sscale_customfactor(variables.font.render("J", 0, variables.WHITE), feedback_factor)
Ktext = sscale_customfactor(variables.font.render("K", 0, variables.WHITE), feedback_factor)
Ltext = sscale_customfactor(variables.font.render("L", 0, variables.WHITE), feedback_factor)
SEMICOLONtext = sscale_customfactor(variables.font.render(";", 0, variables.WHITE), feedback_factor)
PERFECTtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("PERFECT", 0, variables.WHITE), feedback_factor), -45)
OKtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("OK", 0, variables.WHITE), feedback_factor), -45)
GOODtext = pygame.transform.rotate(sscale_customfactor(variables.font.render("GOOD", 0, variables.WHITE), feedback_factor), -45)
MISStext = pygame.transform.rotate(sscale_customfactor(variables.font.render("MISS", 0, variables.WHITE), feedback_factor), -45)

GR = {}
picnames = os.listdir(os.path.dirname(os.path.abspath("__file__")) + "/pics")

def nicename(filename):
    return filename.replace(".png", "").lower()

def addtoGR(filename):
    p = simport(filename)
    GR[nicename(filename)] = p

for x in picnames:
    addtoGR(x)

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
    return GR[nicetreename]

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
    return GR[nicename(filename)]

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
    return GR[nicename(filename)]
