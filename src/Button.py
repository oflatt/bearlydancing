#Oliver Flatt
import variables, pygame
from pygame import Rect
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
            return textpic.get_width() + variables.getbuttonpadding()*2
        else:
            return self.screenwidthoverride * variables.width

    def height(self):
        return self.size*variables.height + 2 * variables.getbuttonpadding()
        

    def draw(self, ison = False):
        if ison:
            rectcolor = variables.BLUE
        else:
            rectcolor = variables.BLUEGREY
            
        if self.iscentered:
            xpos = self.x*variables.width - self.width()/2
            ypos = self.y*variables.height - self.height()/2
        else:
            xpos = self.x*variables.width
            ypos = self.y*variables.height
            
        textpic = getTextPic(self.text, self.size*variables.height)

        textpadding = (self.width() - textpic.get_width()) / 2
        ypadding = (self.height() - textpic.get_height()) / 2
        padding = variables.getbuttonpadding()

        drawrect = Rect(xpos+padding, ypos+padding, self.width()-2*padding, self.height()-2*padding)

        pygame.draw.rect(variables.screen, rectcolor, drawrect, padding)
        pygame.draw.rect(variables.screen, variables.BLUEWHITE, drawrect)

        variables.screen.blit(textpic, [xpos + textpadding, ypos+ypadding])
        
        # just always update screen
        variables.dirtyrects.append(pygame.Rect(xpos-1, ypos-1, self.width()+2, self.height()+2))


