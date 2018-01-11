#Oliver Flatt
import variables, pygame
from graphics import scale_pure, getTextPic

class Button:
    iscentered = False

    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.size = size  # size is a height of the text

        self.assign_text(text)
        textpic = getTextPic(self.text, size)
        
        self.width = textpic.get_width() + variables.buttonpadding
        self.height = textpic.get_height()

    def assign_text(self, text):
        self.text = text
        

    def draw(self, ison = False):
        if ison:
            rectcolor = variables.GREEN
        else:
            rectcolor = variables.WHITE
        if self.iscentered:
            xpos = self.x - self.width/2
            ypos = self.y - self.height/2
        else:
            xpos = self.x
            ypos = self.y
        textpic = getTextPic(self.text, self.size)

        textpadding = (self.width - textpic.get_width()) / 2
        
        pygame.draw.rect(variables.screen, rectcolor, [xpos, ypos, self.width, self.height])
        
        variables.screen.blit(textpic, [xpos + textpadding, ypos])
