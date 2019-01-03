from FrozenClass import FrozenClass
import variables

class Wind(FrozenClass):

    # creates a new wind object, defaulting it at the left side of the screen.
    def __init__(self):

        self.starttime = variables.settings.current_time

        # speed is measured in pixels per second
        self.speed = 1.0

        # a list of WindShifts, which are surfaces and where to blit them
        self.windshifts = []

        self._freeze()

    # returns the position of the wind in pixels
    def windpos(self):
        return (variables.settings.current_time - self.starttime) * self.speed

    def draw(self, mapoffset):
        for w in self.windshifts:
            w.draw(mapoffset)

    def tick(self):
        i = 0
        while i < len(self.windshifts):
            if variables.settings.current_time >= self.windshifts[i].endtime:
                self.windshifts.pop(i)
            else:
                i = i + 1

    def addwindshift(self, windshift):
        self.windshifts.append(windshift)
