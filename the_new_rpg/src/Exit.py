#Oliver Flatt works on classes

class Exit():
    def __init__(self, area, isbutton, name, newx, newy):
        self.area = area #x, y, width, height in a list (a Rect)
        self.isbutton = isbutton #true if you have to hit a button to enter
        self.name = name #name of map it exits to
        self.newx = newx
        self.newy = newy
