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
            # don't start at beginning
            m.firstbootup = False

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()

    return m


class Menu():
    option = 0
    state = "main"
    options = ["resume", "save", "controls", "exit"]
    optionpics = []
    textxoffset = 0
    textyspace = 0
    # if it is true, it is displaying the main menu
    mainmenup = True
    namepics = []
    
    def __init__(self):
        self.playpic = graphics.sscale_customfactor(variables.font.render("play", 0, variables.WHITE), 1)
        for o in self.options:
            textpic = graphics.sscale_customfactor(variables.font.render(o, 0, variables.WHITE), 1)
            self.optionpics.append(textpic)
        nameprompts = ["Your name:", "The sleeping bear's name:"]
        self.namepics = []
        for p in nameprompts:
            textpic = graphics.sscale_customfactor(variables.font.render(p, 0, variables.BLACK), 1)
            self.namepics.append(textpic)

        self.textyspace = variables.font.get_linesize()*variables.height*0.003
        self.textxoffset = self.optionpics[0].get_width() / 6
        self.reset()
        self.mainmenup = True
        self.namestring = ""
        self.shifton = False
        self.backspaceon = False
        self.backspacetime = 0
        self.firstbootup = True

    def ontick(self):
        if self.state == "name":
            if self.backspaceon:
                if (variables.settings.current_time - self.backspacetime) > 200:
                    self.namestring = self.namestring[:-1]
                    self.backspacetime = variables.settings.current_time
        
    def reset(self):
        self.option = 0
        self.state = "main"
        self.enemyanimation = random.choice(enemies.animations)

    def pause(self):
        if (not isinstance(classvar.battle, str)):
            classvar.battle.pause()
        variables.settings.menuonq = not variables.settings.menuonq
        self.reset()
        classvar.player.change_of_state()

    def resume(self):
        if not self.mainmenup:
            self.reset()
            variables.settings.menuonq = False
            classvar.player.change_of_state()
            if not isinstance(classvar.battle, str):
                classvar.battle.unpause()

    def drawmain(self):
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

    # in drawname option is used as how far they have gotten through the process
    def drawname(self):
        textpic = self.namepics[self.option]
        typepic = graphics.sscale_customfactor(variables.font.render(self.namestring, 0, variables.BLACK), 1)
        variables.screen.blit(textpic, [variables.width/2 - textpic.get_width()/2, variables.height/2 - textpic.get_height()*1.5])
        variables.screen.blit(typepic, [variables.width/2 - typepic.get_width()/2, variables.height/2 - textpic.get_height()/2])
            
    def draw(self):
        if self.state == "main":
            self.drawmain()
        else:
            self.drawname()

    def onrelease(self, key):
        if self.state == "name":
            if key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.shifton = False
            elif key == pygame.K_BACKSPACE:
                self.backspaceon = False

    def onkey(self, key):
        if self.state == "main":
            self.onkeymain(key)
        else:
            self.onkeyname(key)

    def onkeyname(self, key):
        if key in variables.settings.enterkeys and key != pygame.K_SPACE:
            if len(self.namestring) != 0:
                self.option += 1
                if self.option == 0:
                    variables.settings.username = self.namestring
                else:
                    variables.settings.bearname = self.namestring
                self.namestring = ""
                if self.option >= len(self.namepics):
                    self.mainmenup = False
                    self.resume()
        elif key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
            self.shifton = True
        elif key in [pygame.K_BACKSPACE]:
            self.namestring = self.namestring[:-1]
            self.backspaceon = True
            self.backspacetime = variables.settings.current_time
        elif len(self.namestring) < 20 and not key in variables.settings.escapekeys:
            toadd = pygame.key.name(key)
            if toadd == "space":
                toadd = " "
            elif self.shifton:
                toadd = toadd.upper()
            self.namestring = self.namestring + toadd
        

    def onkeymain(self, key):
        if key in variables.settings.upkeys:
            self.option = (self.option - 1) % len(self.options)
        elif key in variables.settings.downkeys:
            self.option = (self.option + 1) % len(self.options)
        elif key in variables.settings.enterkeys:
            if self.options[self.option] == "resume":
                if self.mainmenup and self.firstbootup:
                    self.state = "name"
                    self.option = 0
                else:
                    self.mainmenup = False
                    self.resume()
