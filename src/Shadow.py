from FrozenClass import FrozenClass

class Shadow(FrozenClass):

    def __init__(self, surface, xoffset, yoffset):
        self.surface = surface
        
        # xoffset and yoffset are for positioning correctly relative to the base of the object, calculated when the shadow is created
        self.xoffset = xoffset
        self.yoffset = yoffset
