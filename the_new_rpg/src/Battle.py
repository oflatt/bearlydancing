#!/usr/bin/python
#Oliver works on classes
import variables, pygame, stathandeling, classvar

class Battle():
    def __init__(self, enemy):
        self.enemy = enemy
        self.state = "choose"
        self.option = 1

    def draw(self):
        h = variables.height
        w = variables.width
        b = h*13/16
        p = classvar.player
        #background
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, w, h])

        if self.state == "choose":
            if self.option == 1:
                dancerectcolor = variables.GREEN
                fleerectcolor = variables.WHITE
            else:
                dancerectcolor = variables.WHITE
                fleerectcolor = variables.GREEN
            pygame.draw.rect(variables.screen, dancerectcolor, [w/10, b, w/2 - (w/5), h*3/16 - h/10])
            pygame.draw.rect(variables.screen, fleerectcolor, [w/2+w/10, b, w/2 - (w/5), h*3/16 - h/10])
            dancepic = variables.font.render("DANCE!", 0, variables.BLACK)
            dance = pygame.transform.scale(dancepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            fleepic = variables.font.render("flee....", 0, variables.BLACK)
            flee = pygame.transform.scale(fleepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            variables.screen.blit(dance, [w/10, b])
            variables.screen.blit(flee, [w/2+w/10, b])

        epic = self.enemy.pic
        variables.screen.blit(epic, [w-epic.get_width(), 0])

        healthh = h*(1/18)
        percenthealthleft = p.health/stathandeling.max_health(p.lv)
        if percenthealthleft<=0.2:
            healthbarcolor = variables.RED
        else:
            healthbarcolor = variables.GREEN
        pygame.draw.rect(variables.screen, healthbarcolor, [0,
                                                            h-healthh,
                                                            w*percenthealthleft,
                                                            healthh])


    def onkey(self, key):
        if self.state == "choose":
            if key == pygame.K_SPACE:
                if self.option == 1:
                    self.state = "dance"
                else:
                    variables.state = "world"
            else:
                if self.option == 1:
                    self.option = 2
                else:
                    self.option = 1
