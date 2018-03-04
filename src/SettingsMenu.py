import variables, pygame, copy
from graphics import getTextPic
from FrozenClass import FrozenClass


class SettingsMenu(FrozenClass):
    def __init__(self):
        self.option = 0
        self.scroll = 0
        self.bindingoption = 0
        self.confirmoption = 0
        # when keys are hit
        self.lefttime = None
        self.righttime = None
        self.uptime = None
        self.downtime = None

        self.confirmationtime = None
        self.state = "main" # can be main, keychange, or confirm

        self.workingcopy = variables.settings.keydict # a copy is created with the first edit
        
        self._freeze()

    def draw(self):
        options = list(self.workingcopy.keys()) + ["back"]
        if self.state == "main":

            onscreen = options[self.scroll:self.scroll+self.linesperscreen()]
            for i in range(len(onscreen)):
                ypos = i* variables.getmenutextyspace()
                keytype = onscreen[i]
                # if it is the back button
                if keytype == options[-1]:
                    title = getTextPic(keytype, variables.textsize, variables.WHITE)
                    variables.screen.blit(title, (variables.getmenutextxoffset(), ypos))
                    if i == self.option-self.scroll:
                        self.drawdot(variables.getmenutextxoffset())
                else:
                    if i == self.option-self.scroll:
                        self.drawline(keytype, ypos, selectedoption = self.bindingoption)
                    else:
                        self.drawline(keytype, ypos)
                        
        elif self.state == "keychange":
            text = getTextPic("Press a key to bind to " + options[self.option], variables.textsize, variables.WHITE)
            variables.screen.blit(text, (variables.width/2 - text.get_width()/2, variables.height/2 - text.get_height()/2))

        elif self.state == "confirm":
            text = getTextPic("Continue with these settings?", variables.textsize, variables.WHITE)
            variables.screen.blit(text, (variables.width/2 - text.get_width()/2, variables.height/2 - variables.textsize*2))
            counter = getTextPic(str(self.confirmsecondsleft()), variables.textsize, variables.WHITE)
            variables.screen.blit(counter, (variables.width/2 - counter.get_width()/2, variables.height/2 - variables.textsize/2))

            yesnoy = variables.height/2 + variables.textsize*2
            yes = getTextPic("yes", variables.textsize, variables.WHITE)
            yesx = variables.width/2 - yes.get_width() - variables.getmenutextxoffset()
            variables.screen.blit(yes, (yesx, yesnoy))

            no = getTextPic("no", variables.textsize, variables.WHITE)
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
        dotwidth = variables.getmenutextxoffset() * 1/3
        pygame.draw.rect(variables.screen, variables.WHITE,
                         [xpos - dotwidth,
                          ypos,
                          dotwidth,
                          dotwidth])
        
    def linesperscreen(self):
        return int(variables.height/(variables.getmenutextyspace()))
        
    def drawline(self, keytype, ypos, selectedoption = None):
        title = getTextPic(keytype + "-", variables.textsize, variables.WHITE)
        variables.screen.blit(title, (variables.getmenutextxoffset(), ypos))
        keylist = ["X"] + self.workingcopy[keytype] + ["+"]
        
        i = 0
        currentx = variables.getmenutextxoffset()*2 + title.get_width()
        while i < len(keylist):
            if i == selectedoption:
                self.drawdot(currentx)
            if i == len(keylist)-1:
                textstring = keylist[i]
            elif i == 0:
                textstring = keylist[i]
            else:
                textstring = pygame.key.name(keylist[i])
            
            textpic = getTextPic(textstring, variables.textsize, variables.WHITE)
                
            variables.screen.blit(textpic, (currentx, ypos))
            currentx += variables.getmenutextxoffset()+textpic.get_width()
                
            i += 1

    def getcurrentoptionbindings(self):
        options = list(self.workingcopy.keys()) + ["back"]
        if self.option == len(options)-1:
            return []
        else:
            return self.workingcopy[options[self.option]]

    # returns a message to set or None
    def onkey(self, key):
        if self.state == "main":
            message = None
            optionslength = len(self.workingcopy) + 1
            # if on the back button
            if self.option == optionslength-1:
                linelength = 1
            else:
                linelength = len(self.getcurrentoptionbindings()) + 3

            if variables.checkkey("up", key):
                self.uptime = variables.settings.current_time
                if self.option <= 0:
                    self.scroll = optionslength-self.linesperscreen()
                self.option = (self.option - 1) % optionslength
                if self.option < self.scroll:
                    self.scroll -= 1
                self.bindingoption = 0
            elif variables.checkkey("down", key):
                self.downtime = variables.settings.current_time
                if self.option >= optionslength-1:
                    self.scroll = 0
                self.option = (self.option + 1) % optionslength
                if self.option > self.scroll + self.linesperscreen()-1:
                    self.scroll += 1
            elif variables.checkkey("left", key):
                bindingslength = len(self.getcurrentoptionbindings()) + 2
                self.lefttime = variables.settings.current_time
                self.bindingoption = (self.bindingoption - 1) % bindingslength
            elif variables.checkkey("right", key):
                bindingslength = len(self.getcurrentoptionbindings()) + 2
                self.righttime = variables.settings.current_time
                self.bindingoption = (self.bindingoption + 1) % bindingslength

            elif variables.checkkey("enter", key):
                bindingslength = len(self.getcurrentoptionbindings()) + 2
                if bindingslength-1 > self.bindingoption > 0:
                    self.initiatekeychange()
                elif self.option == optionslength - 1:
                    self.initiateconfirm()

            elif variables.checkkey("escape", key):
                self.initiateconfirm()

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
                return key in self.workingcopy[name]
            
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
                    variables.settings.keydict = self.workingcopy
                    message = "confirmed new settings"

            return message

    def initiateconfirm(self):
        # start on no
        self.confirmoption = 1
        self.confirmationtime = variables.settings.current_time
        self.state = "confirm"
        self.clearkeys()

    def notconfirm(self):
        self.state = "main"
        self.clearkeys()
        
    def initiatekeychange(self):
        if self.workingcopy is variables.settings.keydict:
            self.workingcopy = copy.deepcopy(variables.settings.keydict)
        self.state = "keychange"
        self.clearkeys()

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
