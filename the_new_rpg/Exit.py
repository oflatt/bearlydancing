#Oliver Flatt works on classes

class Exit():
    def __init__(self, area, isbutton, name):
        self.area = area #x, y, x, y in a list
        self.isbutton = isbutton #true if you have to hit a button to enter
        self.name = name #name of map it exits to
