#Oliver Flatt
import variables, pygame, graphics

class Button:
    ison = False
    iscentered = True

    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.text = text
        self.size = size #size multiplies the default size

    def draw(self):
        if self.ison:
            rectcolor = variables.GREEN
        else:
            rectcolor = variables.WHITE
        textpic = graphics.sscale_customfactor(variables.font.render(self.text, 0, variables.BLACK), self.size)
        tw = textpic.get_width()
        th = textpic.get_height()
        if self.iscentered:
            xpos = self.x - tw/2
            ypos = self.y - th/2
        else:
            xpos = self.x
            ypos = self.y
        pygame.draw.rect(variables.screen, rectcolor, [xpos, ypos, tw, th])
        variables.screen.blit(textpic, [xpos, ypos])