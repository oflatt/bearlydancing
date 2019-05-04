#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, classvar, initiatebattle
from ChoiceButtons import ChoiceButtons
from graphics import scale_pure, getpic, getTextPic
from FrozenClass import FrozenClass

class Speak(FrozenClass):

    def __init__(self, pic, dialogue, side = None, bottomp = True, options = [], special_battle = "none"):
        if pic == None:
            self.pic = "empty"
        else:
            self.pic = pic

        # dialogue is a list of strings, one per line
        if type(dialogue) == str:
            self.dialogue = [dialogue]
        else:
            self.dialogue = dialogue
        self.side = side
        # a list of keys that work to exit the conversation- keys acceced in settings keydict
        self.specialexitkeys = None
        self.bottomp = bottomp
        self.releaseexit = False

        self.line = 0
        self.releaseexit = False
        self.dialogue_initializedp = False
        # set to true on the first draw, and lines get wrapped
        self.lines_wrappedp = False

        self.state = "talking"

        # options is a list of text for buttons to be displayed at the end of the speak
        self.options = options
        self.choicebuttons = None
        if len(self.options)>0:
            self.choicebuttons = ChoiceButtons(self.options,
                                               1- variables.gettextsize()/variables.height-1/20)
            # start on second option
            self.choicebuttons.nextoption()
            
        self.special_battle = special_battle

        self._freeze()

    def reset(self):
        self.line = 0
        self.state = "talking"

    def wraplines(self):
        if self.lines_wrappedp:
            return
        
        index = 0
        while index < len(self.dialogue):
            linedrawn = self.linepic(index)
            if linedrawn.get_width() > variables.width:
                cutpoint = int(len(self.dialogue[index])/2)
                self.dialogue.insert(index+1, self.dialogue[index][cutpoint:])
                self.dialogue[index] = self.dialogue[index][:cutpoint] + "-"
            else:
                index += 1

        self.lines_wrappedp = True
    
    def linepic(self, index):
        return getTextPic(self.dialogue[index], variables.gettextsize(), variables.WHITE)

    def draw(self):
        self.wraplines()
        
        if not self.dialogue_initializedp:
            self.initialize_dialogue()
        
        yoffset = 0
        if not self.bottomp:
            yoffset = -variables.height + variables.gettextboxheight()
        #text
        line1 = self.linepic(0)
                                
        line_height = line1.get_height()
        h = variables.height
        w = variables.width
        b = h-variables.gettextboxheight()
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b+yoffset, w, variables.gettextboxheight()])
        numoflines = variables.getlinesinscreen()
        if numoflines > len(self.dialogue):
            numoflines = len(self.dialogue)
        for x in range(0, numoflines):
            line = self.linepic(x+self.line)
            variables.screen.blit(line, [w/2 - line.get_width()/2, b+(line_height*x)+yoffset])

        if self.line < len(self.dialogue) - variables.getlinesinscreen():
            arrowpic = getpic("downarrow", variables.displayscale*2)
        else:
            arrowpic = getpic("rightarrow", variables.displayscale*2)
        variables.screen.blit(arrowpic,
                              [variables.width-2*variables.displayscale*2-arrowpic.get_width(),
                               variables.height-2*variables.displayscale*2-arrowpic.get_height()+yoffset])

        if self.state == "choosing":
            self.choicebuttons.draw()

    def keypress(self, key):
        choice = None
        if self.line < len(self.dialogue) - variables.getlinesinscreen():
            self.line += 1
            return "talking"
        # if there is a choice to be made
        elif self.choicebuttons != None:
            if self.state == "talking":
                self.state = "choosing"
            elif self.state == "choosing":
                self.choicebuttons.leftrightonkey(key)
                if variables.checkkey("enter", key):
                    choice = self.choicebuttons.getoption()
                    self.state = "done"
            
        # if there is a specialexitkey, only exit if it is pressed
        elif self.specialexitkeys != None:
            keypressedp = False
            for keytype in self.specialexitkeys:
                if variables.checkkey(keytype, key):
                    keypressedp = True
                    break
            if keypressedp:
                self.state = "done"
        elif variables.checkkey("enter", key):
            self.state = "done"
        
        returnstate = self.state
        
        if self.state == "done":
            if choice in [None, "y", "yes"]:
                if self.special_battle != "none":
                    initiatebattle.initiatebattle(self.special_battle)
                    returnstate = "specialbattle"

            self.reset()
            
            
        return returnstate


    def keyrelease(self, key):
        self.keypress(key)

    # replaces the default name Honey 
    def initialize_dialogue(self):
        for i in range(len(self.dialogue)):
            self.dialogue[i] = self.dialogue[i].replace("Honey", variables.settings.bearname)
            self.dialogue[i] = self.dialogue[i].replace("User", variables.settings.username)
