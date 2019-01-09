from pygame import Rect

from FrozenClass import FrozenClass
from WindShift import WindShift
import variables


# a class that holds all the wind shifts for an object
class WindEffect(FrozenClass):

    def __init__(self):
        self.windshifts = []

    def draw(self, mapoffset, destination = variables.screen):
        # first remove old windshifts
        i = 0
        while i < len(self.windshifts):
            if variables.settings.current_time >= self.windshifts[i].endtime:
                self.windshifts.pop(i)
            else:
                i = i + 1
        
        for w in self.windshifts:
            w.draw(mapoffset, destination = destination)


    def addwindshift(self, windshift):
        self.windshifts.append(windshift)

    def emptyp(self):
        return len(self.windshifts) == 0

    # returns a windshift of the surface from the shiftrect if the rect is valid
    # and has corners touching green
    # if checkpoints is none, it defaults to the top left and bottom right corners
    def windshiftifgreen(self, surface, shiftrect, checkpoints = None,
                         timeoffset = 500, accepttransparent = False):
        baserect = surface.get_rect()

        if checkpoints == None:
            checkpoints = [(shiftrect.x, shiftrect.y),
                           (shiftrect.x+shiftrect.width-1, shiftrect.y+shiftrect.height-1)]
        
        if not baserect.contains(shiftrect):
            return None
    
        for p in checkpoints:
            c = surface.get_at(p)
            if not variables.greenp(c) or (accepttransparent and c[3] == 0):
                return None

        return WindShift(surface.subsurface(shiftrect),
                         (shiftrect[0])/variables.compscale(),
                         (shiftrect[1]-1)/variables.compscale(),
                         variables.settings.current_time + 500)
