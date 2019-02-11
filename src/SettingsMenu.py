import variables, pygame, copy

from graphics import getTextPic
from FrozenClass import FrozenClass
from play_sound import setnewvolume, play_effect

class SettingsMenu(FrozenClass):
    def __init__(self):
        self.option = 0
        self.scroll = 0
        self.bindingoption = 0
        self.bindingscroll = 0
        self.confirmoption = 0
        # when keys are hit
        self.lefttime = None
        self.righttime = None
        self.uptime = None
        self.downtime = None

        self.confirmationtime = None
        self.state = "main" # can be main, keychange, or confirm

        self.workingcopy = variables.settings # a copy is created with the first edit

        self.optionsbeforebindings = ["mode", "volume"]
        self.toggleoptions = ["autosave", "dance pad mode"]
        self.toggleoptionsvars = ["autosavep", "dancepadmodep"]
        self.windowmodes = ["fullscreen", "windowed"]
        self.optionsafterbindings = ["back"]
        
        self._freeze()

    def newworkingcopy(self):
        self.workingcopy = variables.settings

    def draw(self):
        options = self.getoptionlist()
        if self.state == "main":

            onscreen = options[self.scroll:self.scroll+self.linesperscreen()]
            for i in range(len(onscreen)):
                ypos = i * variables.getmenutextyspace()
                keytype = onscreen[i]
                # if it is not a binding
                if not keytype in self.workingcopy.keydict:
                    title = getTextPic(keytype, variables.gettextsize(), variables.WHITE)
                    variables.screen.blit(title, (variables.getmenutextxoffset(), ypos))
                    # draw dot
                    if i == self.option-self.scroll and keytype != "mode":
                        self.drawdot(variables.getmenutextxoffset())

                    if keytype == "volume":
                        for x in range(int(self.workingcopy.volume*10)):
                            xpos = variables.getmenutextxoffset() + variables.gettextsize()*x + title.get_width()
                            variables.screen.fill(variables.BLUE, (xpos + variables.gettextsize()/4, ypos + variables.gettextsize()/4,
                                                                   variables.gettextsize()*(3/4), variables.gettextsize()*(3/4)))
                    elif keytype == "mode":
                        xpos = variables.getmenutextxoffset()*2 + title.get_width()
                        i = 0
                        for t in self.windowmodes:
                            if i == self.bindingoption:
                                if options[self.option] == "mode":
                                    self.drawdot(xpos, ypos)
                            pic = getTextPic(t, variables.gettextsize(), variables.WHITE)
                            variables.screen.blit(pic, (xpos, ypos))
                            if self.workingcopy.windowmode == t:
                                pygame.draw.rect(variables.screen, variables.BLUE, (xpos-2, ypos+2, pic.get_width()+4, pic.get_height()+2), 2)
                            xpos += variables.getmenutextxoffset() + pic.get_width()
                            i += 1
                    elif keytype in self.toggleoptions:
                        xpos = variables.getmenutextxoffset()*2 + title.get_width()
                        text = "off"
                        if getattr(self.workingcopy, self.toggleoptionsvars[self.toggleoptions.index(keytype)]):
                            text = "on"
                        pic = getTextPic(text, variables.gettextsize(), variables.WHITE)
                        variables.screen.blit(pic, (xpos, ypos))
                        if self.workingcopy.autosavep:
                            pygame.draw.rect(variables.screen, variables.BLUE, (xpos-2, ypos+2, pic.get_width()+4, pic.get_height()+2), 1)
                else:
                    if i == self.option-self.scroll:
                        self.drawline(keytype, ypos, selectedoption = self.bindingoption)
                    else:
                        self.drawline(keytype, ypos)
                        
        elif self.state == "keychange":
            text = getTextPic("Press a key to bind to " + options[self.option], variables.gettextsize(), variables.WHITE)
            variables.screen.blit(text, (variables.width/2 - text.get_width()/2, variables.height/2 - text.get_height()/2))

        elif self.state == "confirm":
            text = getTextPic("Continue with these settings?", variables.gettextsize(), variables.WHITE)
            variables.screen.blit(text, (variables.width/2 - text.get_width()/2, variables.height/2 - variables.gettextsize()*2))
            counter = getTextPic(str(self.confirmsecondsleft()), variables.gettextsize(), variables.WHITE)
            variables.screen.blit(counter, (variables.width/2 - counter.get_width()/2, variables.height/2 - variables.gettextsize()/2))

            yesnoy = variables.height/2 + variables.gettextsize()*2
            yes = getTextPic("yes", variables.gettextsize(), variables.WHITE)
            yesx = variables.width/2 - yes.get_width() - variables.getmenutextxoffset()
            variables.screen.blit(yes, (yesx, yesnoy))

            no = getTextPic("no", variables.gettextsize(), variables.WHITE)
            nox = variables.width/2 + no.get_width() + variables.getmenutextxoffset()
            variables.screen.blit(no, (nox, yesnoy))

            # draw dot next to yes
            if self.confirmoption == 0:
                self.drawdot(yesx, yesnoy)
            elif self.confirmoption == 1:
                self.drawdot(nox, yesnoy)

    def confirmsecondsleft(self):
        return int(variables.confirmduration - (variables.settings.current_time-self.confirmationtime)/1000)

    # xpos is the xpos of the text
    def drawdot(self, xpos, ypos = None):
        if ypos == None:
            ypos = (self.option - self.scroll) * variables.getmenutextyspace()
        dotwidth = variables.getdotwidth()
        pygame.draw.rect(variables.screen, variables.WHITE,
                         [xpos - dotwidth,
                          ypos,
                          dotwidth,
                          dotwidth])
        
    def linesperscreen(self):
        return int(variables.height/(variables.getmenutextyspace()))
        
    def drawline(self, keytype, ypos, selectedoption = None):
        title = getTextPic(keytype + "-", variables.gettextsize(), variables.WHITE)
        variables.screen.blit(title, (variables.getmenutextxoffset(), ypos))
        keylist = ["-"] + self.workingcopy.keydict[keytype] + ["+"]
        
        i = self.bindingscroll
        currentx = variables.getmenutextxoffset()*2 + title.get_width()
        while i < len(keylist):
            textpic = self.gettextpic(i, keylist)
            
            if i == selectedoption:
                self.drawdot(currentx)
                # handle scrolling for next frame
                if currentx + textpic.get_width() > variables.width:
                    self.bindingscroll += 1
            
            
            variables.screen.blit(textpic, (currentx, ypos))
            currentx += variables.getmenutextxoffset()+textpic.get_width()
                
            i += 1

        if self.bindingoption < self.bindingscroll:
            self.bindingscroll -= 1

    def getcurrentoptionbindings(self):
        options = self.getoptionlist()
        if not options[self.option] in self.workingcopy.keydict:
            return []
        else:
            return self.workingcopy.keydict[options[self.option]]

    def getoptionlist(self):
        return self.optionsbeforebindings + self.toggleoptions + list(self.workingcopy.keydict.keys()) + self.optionsafterbindings

    def gettextpic(self, i, keylist):
        if i > len(keylist)-1:
            return None
        else:
            if i == len(keylist)-1:
                textstring = keylist[i]
            elif i == 0:
                textstring = keylist[i]
            elif keylist[i] == None:
                textstring = "none"
            elif type(keylist[i]) == str:
                textstring = keylist[i]
            else:
                textstring = pygame.key.name(keylist[i])

            textpic = getTextPic(textstring, variables.gettextsize(), variables.WHITE)
            return textpic

    def getdotxpos(self):
        i = self.bindingscroll
        currentx = variables.getmenutextxoffset()*2 + title.get_width()
        dotx = currentx
        while i < len(keylist):
            if i == self.bindingoption:
                dotx = currentx
                break
            textpic = gettextstring(i)

            currentx += variables.getmenutextxoffset()+textpic.get_width()
                
            i += 1
        return dotx

    # returns a message to set or None
    def onkey(self, key):
        
        play_effect("onedrum", volumeoverride = self.workingcopy.volume)
        if self.state == "main":
            message = None
            optionslist = self.getoptionlist()
            optionslength = len(optionslist)
            # if on the back button
            bindingslength = len(self.getcurrentoptionbindings()) + 2
            if bindingslength == 2:
                bindingslength = 0
            if optionslist[self.option] == "mode":
                bindingslength = len(self.windowmodes)
            if optionslist[self.option] in self.toggleoptions:
                bindingslength = 1
            
            if variables.checkkey("up", key):
                self.uptime = variables.settings.current_time
                if self.option <= 0:
                    self.scroll = optionslength-self.linesperscreen()
                self.option = (self.option - 1) % optionslength
                if self.option < self.scroll:
                    self.scroll -= 1
                
                if bindingslength == 0:
                    self.bindingoption = 0
                else:
                    self.bindingoption = min(bindingslength-1, self.bindingoption)
                    
            elif variables.checkkey("down", key):
                self.downtime = variables.settings.current_time
                if self.option >= optionslength-1:
                    self.scroll = 0
                self.option = (self.option + 1) % optionslength
                if self.option > self.scroll + self.linesperscreen()-1:
                    self.scroll += 1
                bindlength = len(self.getcurrentoptionbindings())
                if bindingslength == 0:
                    self.bindingoption = 0
                else:
                    self.bindingoption = min(bindingslength-1, self.bindingoption)
                    
            elif variables.checkkey("left", key):
                self.lefttime = variables.settings.current_time
                if bindingslength > 0:
                    self.bindingoption = (self.bindingoption - 1) % bindingslength
                if optionslist[self.option] == "volume":
                    self.changevolume(-1)
                    
            elif variables.checkkey("right", key):
                self.righttime = variables.settings.current_time
                if bindingslength > 0:
                    self.bindingoption = (self.bindingoption + 1) % bindingslength
                if optionslist[self.option] == "volume":
                    self.changevolume(1)
                    
            elif variables.checkkey("enter", key):
                if bindingslength-1 > self.bindingoption > 0:
                    self.initiatekeychange()
                elif optionslist[self.option] == "back":
                    message = self.initiateconfirm()
                elif optionslist[self.option] == "mode":
                    self.changewindowmode()
                elif optionslist[self.option] in self.toggleoptions:
                    self.changingcopy()
                    varname = self.toggleoptionsvars[self.toggleoptions.index(optionslist[self.option])]
                    oldval = getattr(self.workingcopy, varname)
                    setattr(self.workingcopy, varname, not oldval)
                elif self.bindingoption == 0:
                    self.deleteonebinding()
                elif self.bindingoption == bindingslength-1:
                    message = self.addonebinding()

            elif variables.checkkey("escape", key):
                message = self.initiateconfirm()

            return message
        
        elif self.state == "keychange":
            current = self.getcurrentoptionbindings()
            current[self.bindingoption-1] = key
            self.exitkeychange()
            return None

        # for confirming, we use the temporary controls
        elif self.state == "confirm":
            message = None
            def checkkeyworkingcopy(name, key):
                if name == "enter":
                    name = "action" # to make things easier
                return key in self.workingcopy.keydict[name]
            
            if checkkeyworkingcopy("left", key):
                self.uptime = variables.settings.current_time
                self.confirmoption = (self.confirmoption - 1) % 2
            elif checkkeyworkingcopy("right", key):
                self.downtime = variables.settings.current_time
                self.confirmoption = (self.confirmoption + 1) % 2
            elif checkkeyworkingcopy("enter", key):
                if self.confirmoption == 1:
                    self.notconfirm()
                elif self.confirmoption == 0:
                    # put the working copy into effect
                    message = self.implementnewsettings()
                    self.exitsettingsmenu()
                    

            return message

    def initiateconfirm(self):
        if self.workingcopy == variables.settings:
            self.exitsettingsmenu()
            return "confirmed without change"
        else:
            # start on no
            self.confirmoption = 1
            self.confirmationtime = variables.settings.current_time
            self.state = "confirm"
            self.clearkeys()
            return None

    # update settings to match workingcopy
    def implementnewsettings(self):
        message = "confirmed new settings"
        newwindowmode = self.workingcopy.windowmode
        if self.workingcopy.windowmode != variables.settings.windowmode:
            variables.setscreen(newwindowmode)

        if variables.settings.volume != self.workingcopy.volume:
            if not variables.soundinit():
                message = "sound error: no available devices"
            else:
                setnewvolume()
            
        variables.settings = self.workingcopy
        return message

    def exitsettingsmenu(self):
        self.state = "main"
        self.clearkeys()

    def notconfirm(self):
        self.state = "main"
        self.clearkeys()

    def changewindowmode(self):
        newmode = self.windowmodes[self.bindingoption]
        if not self.workingcopy.windowmode == newmode:
            self.changingcopy()
            self.workingcopy.windowmode = newmode
        
    def initiatekeychange(self):
        self.changingcopy()
        self.state = "keychange"
        self.clearkeys()

    def changevolume(self, factor):
        self.changingcopy()
        self.workingcopy.volume = (int(self.workingcopy.volume*10) + factor) / 10
        self.workingcopy.volume = min(max(0.0, self.workingcopy.volume), 1.0)

    def deleteonebinding(self):
        bindings = self.getcurrentoptionbindings()
        if len(bindings) > 1:
            self.changingcopy()
            del bindings[0]

    def changingcopy(self):
        if self.workingcopy is variables.settings:
            self.workingcopy = copy.deepcopy(variables.settings)
            
    def addonebinding(self):
        self.changingcopy()
        bindings = self.getcurrentoptionbindings()
        if len(bindings) < variables.maxbindings:
            bindings.append(None)
            self.bindingoption += 1
            return None
        else:
            return "Maximum of " + str(variables.maxbindings) + " keybindings"

    def exitkeychange(self):
        self.state = "main"

    def onrelease(self, key):
        if variables.checkkey("up", key):
            self.uptime = None
        elif variables.checkkey("down", key):
            self.downtime = None
        elif variables.checkkey("left", key):
            self.lefttime = None
        elif variables.checkkey("right", key):
            self.righttime = None

    def clearkeys(self):
        self.uptime = None
        self.downtime = None
        self.lefttime = None
        self.righttime = None

    def ontick(self):
        t = variables.settings.current_time
        if self.state == "main":
            if self.uptime != None:
                if t-self.uptime > variables.menuscrollspeed:
                    self.onkey(variables.settings.keydict["up"][0])
            elif self.downtime != None:
                if t-self.downtime > variables.menuscrollspeed:
                    self.onkey(variables.settings.keydict["down"][0])
            elif self.lefttime != None:
                if t-self.lefttime > variables.menuscrollspeed:
                    self.onkey(variables.settings.keydict["left"][0])
            elif self.righttime != None:
                if t-self.righttime > variables.menuscrollspeed:
                    self.onkey(variables.settings.keydict["right"][0])

        if self.state == "confirm":
            if self.confirmsecondsleft() <= 0:
                self.notconfirm()
