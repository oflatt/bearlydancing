import graphics, variables, pygame, enemies, classvar, maps, random
from pygame import Rect
from classvar import player
from graphics import getpicbyheight

textsize = variables.height/10

class Menu():
    
    def __init__(self):
        self.option = 0
        self.state = "main"
        self.options = ["resume", "save", "controls", "exit"]
        self.mainmenuoptions = ["play", "controls", "exit"]
        self.optionpics = []
        self.mainmenuoptionpics = []
        self.textxoffset = 0
        self.textyspace = 0
        self.namepics = []

        self.message = None
        self.messagetime = 0
        
        for o in self.mainmenuoptions:
            textpic = graphics.scale_pure(variables.font.render(o, 0, variables.WHITE), textsize)
            self.mainmenuoptionpics.append(textpic)
        for o in self.options:
            textpic = graphics.scale_pure(variables.font.render(o, 0, variables.WHITE), textsize)
            self.optionpics.append(textpic)
        nameprompts = ["Your name:", "The sleeping bear's name:"]
        self.namepics = []
        for p in nameprompts:
            textpic = graphics.scale_pure(variables.font.render(p, 0, variables.BLACK), textsize)
            self.namepics.append(textpic)

        self.textyspace = variables.font.get_linesize()*variables.height*0.003
        self.textxoffset = self.optionpics[0].get_width() / 6
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
            mpic = variables.font.render(self.message, 0, variables.WHITE)
            mpic = graphics.scale_pure(mpic, textsize)
            mx = variables.width/2-mpic.get_width()/2
            my = variables.height/2-mpic.get_height()/2
            variables.screen.fill(variables.BLACK, Rect(mx-extrabuttonwidth,
                                                        my,
                                                        mpic.get_width()+2*extrabuttonwidth,
                                                        mpic.get_height()))
            variables.screen.blit(mpic, [mx, my])
        
        opics = self.optionpics
        if self.mainmenup:
            opics = self.mainmenuoptionpics
            
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
        
        textpic = self.namepics[self.option]
        typepic = graphics.scale_pure(variables.font.render(self.namestring, 0, variables.BLACK), textsize, "height")
        variables.screen.blit(textpic, [variables.width/2 - textpic.get_width()/2, variables.height/2 - textpic.get_height()*1.5])
        variables.screen.blit(typepic, [variables.width/2 - typepic.get_width()/2, variables.height/2 - textpic.get_height()/2])

        if self.message != None:
            mpic = variables.font.render(self.message, 0, variables.WHITE)
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
            if len(self.namestring) != 0:
                # self.namestring = self.namestring[:1].upper() + self.namestring[1:]
                if self.option == 0:
                    variables.settings.username = self.namestring
                    if variables.settings.username.lower() == "tessa":
                        self.setmessage("<3")
                    elif variables.settings.username.lower() == "oliver":
                        self.setmessage("hey that's me!")
                    elif variables.settings.username.lower() == "sophie" or variables.settings.username.lower() == "sophia":
                        self.setmessage("the best sister there is")
                else:
                    variables.settings.bearname = self.namestring

                    
                self.namestring = ""
                self.option += 1
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
