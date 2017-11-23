import graphics, variables, pygame, enemies, pickle, classvar, maps, os, random
from classvar import player


# can't pickle pygame masks, and problems pickeling pygame surfaces
def save(me):
    player.mask = 0
    savelist = [variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress,
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
            variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress, classvar.battle, maps.current_map_name = loadedlist
            maps.change_map(maps.current_map_name, player.xpos, player.ypos)

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()
    return m


class Menu():
    option = 0
    options = ["resume", "save", "controls", "exit"]
    optionpics = []
    textxoffset = 0
    textyspace = 0
    # if it is true, it is displaying the main menu
    mainmenup = True

    def __init__(self):
        self.playpic = graphics.sscale_customfactor(variables.font.render("play", 0, variables.WHITE), 1)
        for o in self.options:
            textpic = graphics.sscale_customfactor(variables.font.render(o, 0, variables.WHITE), 1)
            self.optionpics.append(textpic)

        self.textyspace = variables.font.get_linesize()*variables.height*0.003
        self.textxoffset = self.optionpics[0].get_width() / 6
        self.reset()
        self.mainmenup = True

    def reset(self):
        self.option = 0
        self.enemyanimation = random.choice(enemies.animations)

    def resume(self):
        self.reset()
        self.mainmenup = False
        variables.settings.menuonq = False
        classvar.player.change_of_state()
        if not isinstance(classvar.battle, str):
            classvar.battle.unpause()

    def draw(self):
        xoffset = self.textxoffset
        
        for x in range(len(self.optionpics)):
            textpic = self.optionpics[x]
            
            if self.mainmenup:
                if x == 0:
                    textpic = self.playpic
                xoffset = int(variables.width / 2 - (textpic.get_width() / 2))
            extrabuttonwidth = self.textxoffset / 4
            pygame.draw.rect(variables.screen, variables.BLACK,
                             pygame.Rect(xoffset-extrabuttonwidth,
                                         (x + 1) * self.textyspace,
                                         textpic.get_width() + 2*extrabuttonwidth,
                                         textpic.get_height()))
            variables.screen.blit(textpic,
                                  [xoffset, (x + 1) * self.textyspace])
        dotxoffset = self.textxoffset
        if self.mainmenup:
            if self.option == 0:
                dotxoffset = int(variables.width / 2 - (self.playpic.get_width() / 2))
            else:
                dotxoffset = int(variables.width / 2 - (self.optionpics[self.option].get_width() / 2))
        pygame.draw.rect(variables.screen, variables.WHITE,
                         [dotxoffset - (self.textxoffset * (3/4)), (self.option + 1) * self.textyspace, self.textxoffset * (3 / 4),
                          self.textxoffset * (3 / 4)])
        if self.mainmenup:
            enemyframe = self.enemyanimation.current_frame()["img"]
            variables.screen.blit(enemyframe,
                                  [int(variables.width/2 - enemyframe.get_width()/2), (len(self.optionpics) + 1) * self.textyspace])

    def onkey(self, key):
        if key in variables.settings.upkeys:
            self.option = (self.option - 1) % len(self.options)
        elif key in variables.settings.downkeys:
            self.option = (self.option + 1) % len(self.options)
        elif key in variables.settings.enterkeys:
            if self.options[self.option] == "resume":
                self.resume()
