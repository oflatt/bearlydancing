#Oliver Flatt works on classes
import variables

class Exit():
    def __init__(self, area, isbutton, name, newx, newy):
        self.area = area #x, y, width, height in a list (a Rect)
        self.isbutton = isbutton #true if you have to hit a button to enter
        self.name = name #name of map it exits to
        self.newx = newx
        self.newy = newy

    def scale_by_offset(self, scale):
        s = scale
        self.area = [self.area[0]*s, self.area[1]*s, self.area[2]*s, self.area[3]*s]

