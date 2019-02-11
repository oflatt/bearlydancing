import graphics, variables, pygame, enemies, classvar, maps, random, stathandeling, copy
from pygame import Rect
from classvar import player
from graphics import getpicbyheight, getTextPic, getpic, difficultytocolor
from ChoiceButtons import ChoiceButtons
from SettingsMenu import SettingsMenu
from play_sound import stop_music, play_music, play_effect
from initiatestate import returntoworld

from FrozenClass import FrozenClass

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

# self.state can be main or name
class Menu(FrozenClass):
    
    def __init__(self):
        self.settingsmenu = SettingsMenu()
        
        self.option = 0
        self.state = "main"

        self.message = None
        self.messagetime = 0
        
        self.nameprompts = ["Your name:", "The sleeping bear's name:", "Increase difficulty of game by:",
                            "Confirm difficulty level ",
                            "Wake up the sleeping bear."]
        self.yesno = ChoiceButtons(["yes","no"], 3*variables.gettextsize()/variables.height)
        # so that it starts on "no"
        self.yesno.nextoption()
        self.tempdifficulty = 0
        

        self.enemyanimation = None
        self.reset()

        # if it is true, it is displaying the main menu
        self.mainmenup = True
        self.namestring = ""
        self.shifton = False
        self.backspaceon = False
        self.backspacetime = 0
        self.firstbootup = True

        # keep track of when the menu was turned on
        self.pausetime = None

        self._freeze()

    def options(self):
        if self.mainmenup:
            return ["play", "settings", "exit"]
        elif variables.settings.state == "game":
            return ["resume", "save", "settings", "leave game", "exit"]
        return ["resume", "save", "settings", "exit"]
        

    def setmessage(self, string):
        if string != None:
            self.message = string
            self.messagetime = variables.settings.current_time

    def saved(self):
        self.setmessage("saved!")

    # this is called regardless of if the menu is up or not
    def drawmessage(self):
        if self.message != None:
            if variables.settings.current_time - self.messagetime > 1000:
                self.message = None
        
        # blit message on top
        if self.message != None:
            if self.message == "saved!":
                icon = getTextPic("saved", variables.gettextsize(), variables.WHITE)
                srect = Rect(0, variables.height-icon.get_height(), icon.get_width(), icon.get_height())
                variables.screen.blit(icon, [srect.x, srect.y])
                variables.dirtyrects.append(srect)
            else:
                graphics.drawthismessage(self.message)
            

    def ontick(self):
        
        if self.state == "name":
            if self.backspaceon:
                if (variables.settings.current_time - self.backspacetime) > variables.menuscrollspeed:
                    self.namestring = self.namestring[:-1]
                    self.backspacetime = variables.settings.current_time
        elif self.state == "settings":
            self.settingsmenu.ontick()
        
    def reset(self):
        self.option = 0
        self.state = "main"
        newanim = copy.copy(random.choice(enemies.animations))
        self.enemyanimation = newanim

    def pause(self):
        play_effect("onedrum")
        self.pausetime = variables.settings.current_time
        
        if variables.settings.state == "battle":
            if (not isinstance(classvar.battle, str)):
                classvar.battle.pause()

        if variables.settings.state == "game":
            variables.currentgame().pausefunction(variables.settings.current_time)
        variables.settings.menuonq = not variables.settings.menuonq
        self.reset()
        classvar.player.change_of_state()
        

    def resume(self):
        if self.mainmenup and self.firstbootup:
            self.state = "name"
            self.option = 0
            play_music("bearhome")
            # continue being in menu
            return

        # stop main menu music
        elif maps.current_map_name == "honeyhome" and self.mainmenup:
            play_music("bearhome")
        else:
            stop_music()


        
        self.reset()
        variables.settings.menuonq = False
        
        
        classvar.player.change_of_state()
        if variables.settings.state == "battle":
            if not isinstance(classvar.battle, str):
                classvar.battle.unpause()

            # keep the menu on if it was the main menu, so the player can see first
            if self.mainmenup:
                variables.settings.menuonq = True



        if variables.settings.state == "game":
            variables.currentgame().unpausefunction(variables.settings.current_time)
        self.mainmenup = False

        

    def drawmain(self):
        extrabuttonwidth = variables.getmenutextxoffset() / 4
        
        opics = []
        optionnames = self.options()
        for o in optionnames:
            textpic = getTextPic(o, variables.gettextsize(), variables.WHITE)
            opics.append(textpic)
            
        xoffset = variables.getmenutextxoffset()
        
        for x in range(len(opics)):
            textpic = opics[x]
            
            if self.mainmenup:
                xoffset = int(variables.width / 2 - (textpic.get_width() / 2))
            pygame.draw.rect(variables.screen, variables.BLACK,
                             pygame.Rect(xoffset-extrabuttonwidth,
                                         (x + 1) * variables.getmenutextyspace(),
                                         textpic.get_width() + 2*extrabuttonwidth,
                                         textpic.get_height()))
            variables.screen.blit(textpic,
                                  [xoffset, (x + 1) * variables.getmenutextyspace()])
            
        dotxoffset = variables.getmenutextxoffset()
        dotwidth = variables.getmenutextxoffset() * 1/3
        if self.mainmenup:
            dotxoffset = int(variables.width / 2 - (opics[self.option].get_width() / 2))
        pygame.draw.rect(variables.screen, variables.WHITE,
                         [dotxoffset - dotwidth,
                          (self.option + 1) * variables.getmenutextyspace(),
                          dotwidth,
                          dotwidth])
        
        if self.mainmenup:
            enemyframe = getpicbyheight(self.enemyanimation.current_frame(), variables.height/5)
            variables.screen.blit(enemyframe,
                                  [int(variables.width/2 - enemyframe.get_width()/2), (len(opics) + 1) * variables.getmenutextyspace()])


    # in drawname option is used as how far they have gotten through the process
    def drawname(self):
        promptstring = self.nameprompts[self.option]
        extrabuttonwidth = variables.getmenutextxoffset() / 4
        if self.nameprompts[self.option] == "Confirm difficulty level ":
            reccomendedtext = getTextPic("The reccomended difficulty for new players is 0.", variables.gettextsize(), variables.beginningprompttextcolor)
            variables.screen.blit(reccomendedtext, [variables.width/2 - reccomendedtext.get_width()/2,
                                                    variables.gettextsize()*0])
            self.yesno.draw()
            promptstring = promptstring + str(self.tempdifficulty) + "?"
        
        textpic = getTextPic(promptstring, variables.gettextsize(), variables.beginningprompttextcolor)
        
        typestring = self.namestring
        typecolor = variables.BLACK
        if self.option == 2:
            typestring = str(self.tempdifficulty)
            typecolor = difficultytocolor(self.tempdifficulty/20.0)
                
        typepic = getTextPic(typestring, variables.gettextsize(), typecolor)
        variables.screen.blit(textpic, [variables.width/2 - textpic.get_width()/2, variables.gettextsize()*1.5])
        variables.screen.blit(typepic, [variables.width/2 - typepic.get_width()/2, variables.gettextsize()*2.5])

            
    def draw(self):
        if self.state == "main":
            self.drawmain()
        elif self.state == "settings":
            self.settingsmenu.draw()
        else:
            self.drawname()

        variables.dirtyrects = [Rect(0,0,variables.width, variables.height)]

    def onrelease(self, key):
        if self.state == "name":
            if key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.shifton = False
            elif key == pygame.K_BACKSPACE:
                self.backspaceon = False
        elif self.state == "settings":
            self.settingsmenu.onrelease(key)

    def onkey(self, key):
        if self.state in ["main"]:
            play_effect("onedrum")
        
        if self.state == "main":
            if variables.checkkey("escape", key):
                self.resume()
            else:
                self.onkeymain(key)
        elif self.state == "settings":
            message = self.settingsmenu.onkey(key)
            if message != "confirmed without change":
                self.setmessage(message)

            if message == "confirmed new settings" or message == "confirmed without change":
                self.state = "main"
        else:
            self.onkeyname(key)


    def onkeyname(self, key):
        if variables.checkkey("enter", key) and (key != pygame.K_SPACE or self.option != 0):
            if len(self.namestring) != 0 or self.option>1:
                # self.namestring = self.namestring[:1].upper() + self.namestring[1:]
                if self.option == 0:
                    variables.settings.username = self.namestring
                    if variables.settings.username.lower() == "tessa":
                        self.setmessage("<3")
                    elif variables.settings.username.lower() == "2j":
                        self.setmessage("green beans my friend")
                    elif variables.settings.username.lower() == "oliver":
                        self.setmessage("hey that's me")
                    elif variables.settings.username.lower() == "sophie" or variables.settings.username.lower() == "sophia":
                        self.setmessage("heyo, have fun")
                elif self.option == 1:
                    variables.settings.bearname = self.namestring
                
                    

                    
                self.namestring = ""
                
                if self.nameprompts[self.option] == "Confirm difficulty level ":
                    if self.yesno.getoption() in ["n","no","NO"]:
                        self.option -= 2
                    else:
                        variables.settings.difficulty = self.tempdifficulty
                        classvar.player.exp = stathandeling.lvexp(self.tempdifficulty + 1)
                if self.option == len(self.nameprompts)-1:
                    self.mainmenup = False
                    self.resume()
                else:
                    self.option += 1
                    
                    
        elif key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
            self.shifton = True

        elif key in [pygame.K_BACKSPACE]:
            self.namestring = self.namestring[:-1]
            self.tempdifficulty = int(self.tempdifficulty/10)
            self.backspaceon = True
            self.backspacetime = variables.settings.current_time
        elif len(self.namestring) < 20 and not variables.checkkey("escape", key) and self.option <2:
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
            elif variables.checkkey("up", key):
                self.tempdifficulty += 1
            elif variables.checkkey("down", key) and self.tempdifficulty > 0:
                self.tempdifficulty -= 1
            if self.tempdifficulty > variables.maxdifficulty:
                self.tempdifficulty = variables.maxdifficulty
        elif self.nameprompts[self.option] == "Confirm difficulty level ":
            self.yesno.leftrightonkey(key)


    def onkeymain(self, key):
        optionslength = len(self.options())
        
        if variables.checkkey("up", key):
            self.option = (self.option - 1) % optionslength
        elif variables.checkkey("down", key):
            self.option = (self.option + 1) % optionslength
        elif variables.checkkey("enter", key):
            if self.getoption() in ["resume", "play"]:
                self.resume()
            if self.getoption() == "settings":
                self.state = "settings"
                self.settingsmenu.newworkingcopy()
            if self.getoption() == "leave game":
                returntoworld()
                self.resume()

    def getoption(self):
        return self.options()[self.option]
