import graphics, variables, pygame, enemies


class Menu():
    option = 0
    options = ["resume", "save", "controls", "exit"]
    optionpics = []
    textxoffset = 0
    textyspace = 0

    def __init__(self):
        for o in self.options:
            textpic = graphics.sscale_customfactor(variables.font.render(o, 0, variables.WHITE), 1)
            self.optionpics.append(textpic)

        self.textyspace = self.optionpics[0].get_height() * (3 / 2)
        self.textxoffset = self.optionpics[0].get_width() / 6
        self.reset()

    def reset(self):
        self.option = 0
        self.enemyanimation = enemies.random_enemy()

    def draw(self):
        for x in range(len(self.optionpics)):
            variables.screen.blit(self.optionpics[x],
                                  [self.textxoffset, (x + 1) * self.textyspace - self.optionpics[x].get_height() / 2])

        pygame.draw.rect(variables.screen, variables.BLACK,
                         [self.textxoffset / 4, (self.option + 1) * self.textyspace, self.textxoffset * (3 / 4),
                          self.textxoffset * (3 / 4)])

    def onkey(self, key):
        self.option = (self.option + 1) % len(self.options)
