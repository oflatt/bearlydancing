#!/usr/bin/python

import pygame, os, variables

def sscale(img):
    factor = 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)])

#like sscale but instead of returning a scaled pic, it returns what the dimensions of the new pic would have been
def sscale_dimensions(img):
    factor = 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)]

#sscale means smart scale, Oliver works on this
#this one does not preserve the original pixel size
def sscale_customfactor(img, factor):
    factor = factor * 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = variables.height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)])

#use if you want pictures where the smaller dimension is a set size
def scale_pure(img, s):
    w = img.get_width()
    h = img.get_height()
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller) * s), int((h/smaller) * s)])

def importpic(filename):
    return pygame.image.load(os.path.join('pics', filename)).convert_alpha()

#simport now returns a dictionary with an image and what its new dimensions would be if scaled
def simport(filename):
    p = importpic(filename)
    dimensions = sscale_dimensions(p)
    return {"img":p, "scale-width":dimensions[0], "scale-height":dimensions[1]}

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

for x in picnames:
    p = simport(x)
    nicename = x.replace(".png", "").lower()
    GR[nicename] = p