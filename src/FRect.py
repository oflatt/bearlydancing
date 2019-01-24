from pygame import Rect
from FrozenClass import FrozenClass

class FRect(FrozenClass):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._freeze()

    def scaledup(self, screen, offset = (0, 0)):
        
        return Rect((self.x+offset[0])*screen.get_height(), (self.y+offset[1])*screen.get_height(),
                    self.w*screen.get_height(), self.h*screen.get_height())
    

    def move(self, xoffset, yoffset):
        self.x += xoffset
        self.y += yoffset

    def __getitem__(self, indices):
        if indices == 0:
            return self.x
        if indices == 1:
            return self.y
        if indices == 2:
            return self.w
        if indeces == 3:
            return self.h
        raise ValueError("Got index for FRect that was not in the range [0, 4].")
