import graphics, variables, pygame, enemies, classvar, maps, random, stathandeling
from pygame import Rect
from classvar import player
from graphics import getpicbyheight, getTextPic

textsize = variables.height/10

def keytonum(key):
    numentered = None
    if key == pygame.K_0 or key == pygame.K_KP0:
        numentered = 0
    elif key == pygame.K_1 or key == pygame.K_KP1:
        numentered = 1
    elif key == pygame.K_2 or key == pygame.K_KP2:
        numentered = 2
    elif key == pygame.K_3 or key == pygame.K_KP3:
        numentered = 3
    elif key == pygame.K_4 or key == pygame.K_KP4:
        numentered = 4
    elif key == pygame.K_5 or key == pygame.K_KP5:
        numentered = 5
    elif key == pygame.K_6 or key == pygame.K_KP6:
        numentered = 6
    elif key == pygame.K_7 or key == pygame.K_KP7:
        numentered = 7
    elif key == pygame.K_8 or key == pygame.K_KP8:
        numentered = 8
    elif key == pygame.K_9 or key == pygame.K_KP9:
        numentered = 9
    return numentered

class Menu():
    
    def __init__(self):
        self.option = 0
        self.state = "main"
        self.options = ["resume", "save", "controls", "exit"]
        self.mainmenuoptions = ["play", "controls", "exit"]
        self.textxoffset = 0
        self.textyspace = 0

        self.message = None
        self.messagetime = 0
        
        self.nameprompts = ["Your name:", "The sleeping bear's name:", "Increase difficulty of game by:"]
        self.tempdifficulty = 0
        
        self.textyspace = variables.font.get_linesize()*variables.height*0.003
        self.textxoffset = getTextPic(self.options[0], textsize, variables.WHITE).get_width() / 6
        self.extrabuttonwidth = self.textxoffset / 4
        self.reset()

        # if it is true, it is displaying the main menu
        self.mainmenup = True
        self.namestring = ""
        self.shifton = False
        self.backspaceon = False
        self.backspacetime = 0
        self.firstbootup = True


    def setmessage(self, string):
        self.message = string
        self.messagetime = variables.settings.current_time

    def saved(self):
        self.setmessage("saved!")

    def ontick(self):
        if self.message != None:
            if variables.settings.current_time - self.messagetime > 1000:
                self.message = None
        
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
        extrabuttonwidth = self.extrabuttonwidth

        if self.message != None:
            mpic = variables.font.render(self.message, 0, variables.WHITE).convert()
            mpic = graphics.scale_pure(mpic, textsize)
            mx = variables.width/2-mpic.get_width()/2
            my = variables.height/2-mpic.get_height()/2
            variables.screen.fill(variables.BLACK, Rect(mx-extrabuttonwidth,
                                                        my,
                                                        mpic.get_width()+2*extrabuttonwidth,
                                                        mpic.get_height()))
            variables.screen.blit(mpic, [mx, my])
        
        opics = []
        
        if self.mainmenup:
            for o in self.mainmenuoptions:
                textpic = getTextPic(o, textsize, variables.WHITE)
                opics.append(textpic)
        else:
            for o in self.options:
                textpic = getTextPic(o, textsize, variables.WHITE)
                opics.append(textpic)
            
        xoffset = self.textxoffset
        
        for x in range(len(opics)):
            textpic = opics[x]
            
            if self.mainmenup:
                xoffset = int(variables.width / 2 - (textpic.get_width() / 2))
            pygame.draw.rect(variables.screen, variables.BLACK,
                             pygame.Rect(xoffset-extrabuttonwidth,
                                         (x + 1) * self.textyspace,
                                         textpic.get_width() + 2*extrabuttonwidth,
                                         textpic.get_height()))
            variables.screen.blit(textpic,
                                  [xoffset, (x + 1) * self.textyspace])
        dotxoffset = self.textxoffset
        if self.mainmenup:
            dotxoffset = int(variables.width / 2 - (opics[self.option].get_width() / 2))
        pygame.draw.rect(variables.screen, variables.WHITE,
                         [dotxoffset - (self.textxoffset * (3/4)), (self.option + 1) * self.textyspace, self.textxoffset * (3 / 4),
                          self.textxoffset * (3 / 4)])
        if self.mainmenup:
            enemyframe = getpicbyheight(self.enemyanimation.current_frame(), variables.height/5)
            variables.screen.blit(enemyframe,
                                  [int(variables.width/2 - enemyframe.get_width()/2), (len(opics) + 1) * self.textyspace])

    # in drawname option is used as how far they have gotten through the process
    def drawname(self):
        extrabuttonwidth = self.extrabuttonwidth
        
        textpic = getTextPic(self.nameprompts[self.option], textsize, variables.WHITE)
        
        typestring = self.namestring
        typecolor = variables.BLACK
        if self.option == 2:
            typestring = str(self.tempdifficulty)
            if self.tempdifficulty == 0:
                typecolor = (0, 255, 0)
            elif self.tempdifficulty == 1:
                typecolor = (150, 255, 0)
            elif self.tempdifficulty == 2:
                typecolor = (255, 255, 0)
            elif self.tempdifficulty < 8:
                typecolor = (255, 255-(self.tempdifficulty - 2)*50, 0)
            elif self.tempdifficulty < 13:
                typecolor = (255, 0, 50*(self.tempdifficulty-7))
            elif self.tempdifficulty < 16:
                typecolor = (255-(self.tempdifficulty-13)*70, 0, 255-(self.tempdifficulty-13)*70)
            else:
                typecolor = (0,0,0)
            
        typepic = graphics.scale_pure(variables.font.render(typestring, 0, typecolor).convert(), textsize, "height")
        variables.screen.blit(textpic, [variables.width/2 - textpic.get_width()/2, variables.height/2 - textpic.get_height()*1.5])
        variables.screen.blit(typepic, [variables.width/2 - typepic.get_width()/2, variables.height/2 - textpic.get_height()/2])

        if self.message != None:
            mpic = variables.font.render(self.message, 0, variables.WHITE).convert()
            mpic = graphics.scale_pure(mpic, textsize, "height")
            mx = variables.width/2-mpic.get_width()/2
            my = variables.height/2+mpic.get_height()
            variables.screen.fill(variables.BLACK, Rect(mx-extrabuttonwidth,
                                                        my,
                                                        mpic.get_width()+2*extrabuttonwidth,
                                                        mpic.get_height()))
            variables.screen.blit(mpic, [mx, my])
            
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
            if len(self.namestring) != 0 or self.option>1:
                # self.namestring = self.namestring[:1].upper() + self.namestring[1:]
                if self.option == 0:
                    variables.settings.username = self.namestring
                    if variables.settings.username.lower() == "tessa":
                        self.setmessage("<3")
                    elif variables.settings.username.lower() == "oliver":
                        self.setmessage("hey that's me!")
                    elif variables.settings.username.lower() == "sophie" or variables.settings.username.lower() == "sophia":
                        self.setmessage("the best sister there is")
                elif self.option == 1:
                    variables.settings.bearname = self.namestring
                else:
                    variables.settings.difficulty = self.tempdifficulty
                    classvar.player.lv = stathandeling.lvexp(self.tempdifficulty)

                    
                self.namestring = ""
                self.option += 1
                if self.option >= len(self.nameprompts):
                    self.mainmenup = False
                    self.resume()
                    
        elif key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
            self.shifton = True
            
        elif key in [pygame.K_BACKSPACE]:
            self.namestring = self.namestring[:-1]
            self.tempdifficulty = int(self.tempdifficulty/10)
            self.backspaceon = True
            self.backspacetime = variables.settings.current_time
        elif len(self.namestring) < 20 and not key in variables.settings.escapekeys and self.option <2:
            toadd = pygame.key.name(key)
            if toadd == "space":
                toadd = " "
            elif self.shifton:
                toadd = toadd.upper()
            self.namestring = self.namestring + toadd
        elif self.option == 2:
            numentered = keytonum(key)
            if not numentered == None:
                if self.tempdifficulty == 0:
                    self.tempdifficulty = numentered
                else:
                    self.tempdifficulty = self.tempdifficulty * 10 + numentered
            elif key in variables.settings.upkeys:
                self.tempdifficulty += 1
            elif key in variables.settings.downkeys and self.tempdifficulty > 0:
                self.tempdifficulty -= 1
            if self.tempdifficulty > variables.maxdifficulty:
                self.tempdifficulty = variables.maxdifficulty
        

    def onkeymain(self, key):
        optionslength = len(self.options)
        if self.mainmenup:
            optionslength = len(self.mainmenuoptions)
        if key in variables.settings.upkeys:
            self.option = (self.option - 1) % optionslength
        elif key in variables.settings.downkeys:
            self.option = (self.option + 1) % optionslength
        elif key in variables.settings.enterkeys:
            if self.getoption() in ["resume", "play"]:
                if self.mainmenup and self.firstbootup:
                    self.state = "name"
                    self.option = 0
                else:
                    self.mainmenup = False
                    self.resume()

    def getoption(self):
        if self.mainmenup:
            return self.mainmenuoptions[self.option]
        else:
            return self.options[self.option]
