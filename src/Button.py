#Oliver Flatt
import variables, pygame
from graphics import scale_pure, getTextPic
from FrozenClass import FrozenClass

class Button(FrozenClass):

    # x and y are relative to the size of the screen- multipliers
    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.size = size  # size is a height of the text as a multiplier of height
        self.screenwidthoverride = None
        self.assign_text(text)
        self.iscentered = False

        self._freeze()

    def assign_text(self, text):
        self.text = text

    def width(self):
        if self.screenwidthoverride == None:
            textpic = getTextPic(self.text, self.size*variables.height)
            return textpic.get_width() + variables.getbuttonpadding()
        else:
            return self.screenwidthoverride * variables.width

    def height(self):
        return self.size*variables.height
        

    def draw(self, ison = False):
        if ison:
            rectcolor = variables.GREEN
        else:
            rectcolor = variables.WHITE
            
        if self.iscentered:
            xpos = self.x*variables.width - self.width()/2
            ypos = self.y*variables.height - self.height()/2
        else:
            xpos = self.x*variables.width
            ypos = self.y*variables.height
            textpic = getTextPic(self.text, self.size*variables.height)

        textpadding = (self.width() - textpic.get_width()) / 2


        variables.screen.fill(rectcolor, [xpos, ypos, self.width(), self.height()])

        
        variables.screen.blit(textpic, [xpos + textpadding, ypos])


