#Oliver Flatt
import variables, pygame, graphics

class Button:
    iscentered = False

    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.size = size  # size multiplies the default size

        self.assign_text(text)
        
        self.width = self.textpic.get_width() + variables.buttonpadding
        self.height = self.textpic.get_height()

    def assign_text(self, text):
        self.text = text
        self.textpic = graphics.sscale_customfactor(variables.font.render(self.text, 0, variables.BLACK), self.size)
        

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

        textpadding = (self.width - self.textpic.get_width()) / 2
        
        pygame.draw.rect(variables.screen, rectcolor, [xpos, ypos, self.width, self.height])
        
        variables.screen.blit(self.textpic, [xpos + textpadding, ypos])
