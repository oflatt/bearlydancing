#!/usr/bin/python
#Oliver Flatt works on Classes
import pygame, variables

class Map():
    def __init__(self, base, terrain):
        #base is a png
        self.base = base
        #terrain is a list of Rock
        self.terrain= terrain

    #x and y are the player's x and y pos
    def draw(self, x, y):
        w = self.base.get_width()
        h = self.base.get_height()
        if x < variables.hh: #if it is in the left side of the map
            drawx = 0 #do not scroll the map at all
        elif x > (w - variables.hh): #if it is on the right side of the map
            drawx = w - variables.height #set it to the maximum scroll
        else:
            drawx = x - variables.hh #otherwise, scroll it by pos (accounting for the initial non-scolling area
        if y < variables.hh: #same but for y pos
            drawy = 0
        elif y > (h - variables.hh):
            drawy = h - variables.height
        else:
            drawy = y - variables.hh
        variables.screen.blit(self.base, [-drawx, -drawy])
        #need to draw all Rock too