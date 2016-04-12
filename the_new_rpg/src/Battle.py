#!/usr/bin/python
#Oliver works on classes
import variables, pygame

class Battle():
    def __init__(self, enemy):
        self.enemy = enemy

    def draw(self):
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, variables.width, variables.height])