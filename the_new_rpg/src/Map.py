#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, classvar
from Exit import Exit

def draw_map(b, t):
    i = b
    for x in range(0, len(t)):
        r = t[x]
        i.blit(r.base, [r.x, r.y])
    return i

class Map():
    startpoint = [10, 10] #xy coordinates of spawn point
    exitareas = []#list of exit
    enemies = []

    def __init__(self, base, terrain):
        #base is a png
        self.base = base
        #terrain is a list of Rock
        self.terrain= terrain
        self.finalimage = draw_map(base, terrain)

    #x and y are the player's x and y pos
    def draw(self, x, y):
        w = self.finalimage.get_width()
        h = self.finalimage.get_height()
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

    def scale_by_offset(self):
        self.finalimage = pygame.transform.scale(self.finalimage, [int(self.finalimage.get_width()*variables.scaleoffset),
                                                 int(self.finalimage.get_height()*variables.scaleoffset)])

    def checkexit(self):
        currentexit = False
        for x in range(0, len(self.exitareas)):
            e = self.exitareas[x]
            p = classvar.player
            s = variables.scaleoffset
            if (p.xpos+p.normal_width) >= e.area[0]*s and p.xpos<=(e.area[2]*s) \
                and (p.ypos + p.normal_height)>=e.area[1]*s and p.ypos<=(e.area[3]*s):
                currentexit = e
                x = len(self.exitareas)
        return currentexit