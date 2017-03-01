#Oliver Flatt
import variables, pygame, graphics

class Button:
    ison = False
    iscentered = False

    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.text = text
        self.size = size  # size multiplies the default size
        self.textpic = graphics.sscale_customfactor(variables.font.render(self.text, 0, variables.BLACK), self.size)
        self.tw = self.textpic.get_width()
        self.th = self.textpic.get_height()

    def draw(self):
        if self.ison:
            rectcolor = variables.GREEN
        else:
            rectcolor = variables.WHITE
        if self.iscentered:
            xpos = self.x - self.tw/2
            ypos = self.y - self.th/2
        else:
            xpos = self.x
            ypos = self.y
        pygame.draw.rect(variables.screen, rectcolor, [xpos, ypos, self.tw, self.th])
        variables.screen.blit(self.textpic, [xpos, ypos])