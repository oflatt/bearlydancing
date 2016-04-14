#!/usr/bin/python
#Oliver works on classes
import variables, pygame, graphics

class Battle():
    def __init__(self, enemy):
        self.enemy = enemy
        self.state = "choose"

    def draw(self):
        h = variables.height
        w = variables.height
        b = h*13/16
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, w, h])
        if self.state == "choose":
            pygame.draw.rect(variables.screen, variables.WHITE, [w/10, b, w/2 - (w/5), h*3/16 - h/10])
            pygame.draw.rect(variables.screen, variables.WHITE, [w/2+w/10, b, w/2 - (w/5), h*3/16 - h/10])
            dancepic = variables.font.render("DANCE!", 0, variables.BLACK)
            dance = pygame.transform.scale(dancepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            fleepic = variables.font.render("flee....", 0, variables.BLACK)
            flee = pygame.transform.scale(fleepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            variables.screen.blit(dance, [w/10, b])
            variables.screen.blit(flee, [w/2+w/10, b])
        epic = self.enemy.pic
        variables.screen.blit(epic, [w-epic.get_width(), 0])
