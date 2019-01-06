from FrozenClass import FrozenClass
import variables


# a class that holds all the wind shifts for an object
class WindEffect(FrozenClass):

    def __init__(self):
        self.windshifts = []

    def draw(self, mapoffset):
        # first remove old windshifts
        i = 0
        while i < len(self.windshifts):
            if variables.settings.current_time >= self.windshifts[i].endtime:
                self.windshifts.pop(i)
            else:
                i = i + 1
        
        for w in self.windshifts:
            w.draw(mapoffset)


    def addwindshift(self, windshift):
        self.windshifts.append(windshift)
