from FrozenClass import FrozenClass

class WindShift(FrozenClass):

    def __init__(self, surface, xpos, ypos, endtime):
        # surface to blit
        self.surface = surface

        # map coordinates in pixels
        self.xpos = xpos
        self.ypos = ypos

        # when it expires
        self.endtime = endtime
        

        self._freeze()
