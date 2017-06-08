#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, graphics

class Speak():
    side = None
    line = 0
    textsize = 0.5

    def __init__(self, pic, dialogue):
        #dialogue is a list of strings, one per line. Writer has to make sure they fit
        self.pic = graphics.scale_pure(pic["img"], variables.photo_size)
        self.dialogue = dialogue

    def lines_in_sceen(self):
        line1 = graphics.sscale_customfactor(variables.font.render(self.dialogue[0], 0, variables.WHITE), self.textsize)
        return int(variables.textbox_height/line1.get_height())

    def draw(self):
        #text
        line1 = graphics.sscale_customfactor(variables.font.render(self.dialogue[0], 0, variables.WHITE), self.textsize)
        line_height = line1.get_height()
        h = variables.height
        w = variables.width
        b = h-variables.textbox_height
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b, w, h])
        numoflines = self.lines_in_sceen()
        if numoflines > len(self.dialogue):
            numoflines = len(self.dialogue)
        for x in range(0, numoflines):
            text = variables.font.render(self.dialogue[self.line+x], 0, variables.WHITE)
            line = graphics.sscale_customfactor(text, self.textsize)
            variables.screen.blit(line, [w/2 - line.get_width()/2, b+(line_height*x)])

    def keypress(self, key):
        if self.line < len(self.dialogue) - self.lines_in_sceen():
            self.line += 1
            return "talking"
        elif key in variables.settings.enterkeys:
            self.line = 0
            return "done"
