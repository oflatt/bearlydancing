#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame
from graphics import scale_pure, getpic
from variables import displayscale, textsize

class Speak():

    def __init__(self, pic, dialogue, side = None, bottomp = True, options = [], special_battle = "none"):
        self.pic = pic

        # dialogue is a list of strings, one per line. Writer has to make sure they fit
        self.dialogue = dialogue
        self.side = side
        # can be a list of keys that work to exit the conversation
        self.specialexitkeys = None
        self.bottomp = bottomp
        self.releaseexit = False

        self.line = 0
        self.releaseexit = False
        self.dialogue_initializedp = False
        self.wraplines()

        # options is a list of text for buttons to be displayed at the end of the speak
        self.options = options
        self.current_option = 0
        self.special_battle = special_battle

    def wraplines(self):
        index = 0
        while index < len(self.dialogue):
            linedrawn = self.drawline(index)
            if linedrawn.get_width() > variables.width:
                cutpoint = int(len(self.dialogue[index])/2)
                self.dialogue.insert(index+1, self.dialogue[index][cutpoint:])
                self.dialogue[index] = self.dialogue[index][:cutpoint] + "-"
            else:
                index += 1
            
    def drawline(self, index):
        return scale_pure(variables.font.render(self.dialogue[index], 0, variables.WHITE),
                                             textsize, "height")

    def draw(self):
        if not self.dialogue_initializedp:
            self.initialize_dialogue()
        
        yoffset = 0
        if not self.bottomp:
            yoffset = -variables.height + variables.textbox_height
        #text
        line1 = self.drawline(0)
                                
        line_height = line1.get_height()
        h = variables.height
        w = variables.width
        b = h-variables.textbox_height
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b+yoffset, w, variables.textbox_height])
        numoflines = variables.lines_in_screen
        if numoflines > len(self.dialogue):
            numoflines = len(self.dialogue)
        for x in range(0, numoflines):
            line = self.drawline(x+self.line)
            variables.screen.blit(line, [w/2 - line.get_width()/2, b+(line_height*x)+yoffset])

        if self.line < len(self.dialogue) - variables.lines_in_screen:
            arrowpic = getpic("downarrow", displayscale*2)
        else:
            arrowpic = getpic("rightarrow", displayscale*2)
        variables.screen.blit(arrowpic,
                              [variables.width-2*displayscale*2-arrowpic.get_width(),
                               variables.height-2*displayscale*2-arrowpic.get_height()])

    def keypress(self, key):
        if self.line < len(self.dialogue) - variables.lines_in_screen:
            self.line += 1
            return "talking"
        elif self.specialexitkeys != None:
            if key in self.specialexitkeys:
                self.line = 0
                return "done"
        elif key in variables.settings.enterkeys:
            self.line = 0
            return "done"

    def keyrelease(self, key):
        self.keypress(key)

    # replaces the default name Honey 
    def initialize_dialogue(self):
        for i in range(len(self.dialogue)):
            self.dialogue[i] = self.dialogue[i].replace("Honey", variables.settings.bearname)
            self.dialogue[i] = self.dialogue[i].replace("User", variables.settings.username)
