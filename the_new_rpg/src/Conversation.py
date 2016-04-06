#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame

class Conversation():
    def __init__(self, dialogue):
        #dialogue is a list of strings, one per line. Writer has to make sure they fit
        self.dialogue = dialogue

    def draw(self):
        h = variables.height
        w = variables.height
        pygame.draw.rect(variables.screen, variables.WHITE, [0, h*3/4, w, h])