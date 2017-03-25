import graphics, variables, pygame, enemies, pickle, classvar, maps, os
from classvar import player


# can't pickle pygame masks, and problems pickeling pygame surfaces
def save(me):
    player.mask = 0
    savelist = [me, variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress,
                classvar.battle, maps.current_map_name]
    with open("bdsave0.txt", "wb") as f:
        pickle.dump(savelist, f)
    player.scale_by_offset()


def load():
    m = Menu()
    if (os.path.isfile(os.path.abspath("bdsave0.txt"))):
        if os.path.getsize(os.path.abspath("bdsave0.txt")) > 0:
            f = open("bdsave0.txt", "rb")
            loadedlist = pickle.load(f)
            m, variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress, classvar.battle, maps.current_map_name = loadedlist
            maps.change_map(maps.current_map_name, player.xpos, player.ypos)

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()

    # make the menu not on
    variables.settings.menuonq = False
    return m


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

        self.textyspace = variables.font.get_linesize()*variables.height*0.0025
        self.textxoffset = self.optionpics[0].get_width() / 6
        self.reset()

    def reset(self):
        self.option = 0
        self.enemyanimation = enemies.random_enemy("woods")

    def resume(self):
        self.reset()
        variables.settings.menuonq = False
        classvar.player.change_of_state()
        if not isinstance(classvar.battle, str):
            classvar.battle.unpause()

    def draw(self):
        for x in range(len(self.optionpics)):
            pygame.draw.rect(variables.screen, variables.BLACK,
                             pygame.Rect(self.textxoffset, (x + 1) * self.textyspace, self.optionpics[x].get_width(),
                                         self.optionpics[x].get_height()))
            variables.screen.blit(self.optionpics[x],
                                  [self.textxoffset, (x + 1) * self.textyspace])

        pygame.draw.rect(variables.screen, variables.WHITE,
                         [self.textxoffset / 4, (self.option + 1) * self.textyspace, self.textxoffset * (3 / 4),
                          self.textxoffset * (3 / 4)])

    def onkey(self, key):
        if key in variables.settings.upkeys:
            self.option = (self.option - 1) % len(self.options)
        elif key in variables.settings.downkeys:
            self.option = (self.option + 1) % len(self.options)
        elif key in variables.settings.enterkeys:
            if self.options[self.option] == "resume":
                self.reset()
                variables.settings.menuonq = False
                classvar.player.change_of_state()
                if (not isinstance(classvar.battle, str)):
                    classvar.battle.unpause()
