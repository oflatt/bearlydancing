#!/usr/bin/python
#Oliver Flatt works on Classes
import variables

def draw_map(b, t):
    i = b
    for x in range(0, len(t)):
        r = t[x]
        i.blit(r.base, [r.x, r.y])
    return i

class Map():
    startpoint = [10, 10] #xy coordinates of spawn point
    exitarea = [80, 80, 100, 100] #two sets of coordinates, specifying an area for the exit. x, y, x, y
    enemies = []

    def __init__(self, base, terrain):
        #base is a png
        self.base = base
        #terrain is a list of Rock
        self.terrain= terrain
        self.finalimage = draw_map(base, terrain)

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

        variables.screen.blit(self.finalimage, [-drawx, -drawy])