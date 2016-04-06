#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, graphics

class Conversation():
    line = 0

    def __init__(self, dialogue, pics):
        #dialogue is a list of strings, one per line. Writer has to make sure they fit
        self.dialogue = dialogue
        self.pics = pics

    def draw(self):
        h = variables.height
        w = variables.height
        b = h*13/16
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b, w, h])
        line1 = graphics.sscale(variables.font.render(self.dialogue[self.line], 0, variables.WHITE))
        line2 = graphics.sscale(variables.font.render(self.dialogue[self.line+1], 0, variables.WHITE))
        line3 = graphics.sscale(variables.font.render(self.dialogue[self.line+2], 0, variables.WHITE))
        variables.screen.blit(line1, [w/2 - line1.get_width()/2, b])
        variables.screen.blit(line2, [w/2 - line2.get_width()/2, b+line1.get_height()])
        variables.screen.blit(line3, [w/2 - line3.get_width()/2, b+line1.get_height()+line2.get_height()])