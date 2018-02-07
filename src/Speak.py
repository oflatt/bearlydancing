#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, classvar
from Battle import Battle
from ChoiceButtons import ChoiceButtons
from graphics import scale_pure, getpic, getTextPic
from variables import displayscale, textsize

# the other entrance into battles is in map
def initiatebattle(enemy, storypenalty):
    variables.settings.state = "battle"
    classvar.player.change_of_state()
    enemy.sethealth()
    classvar.player.heal()
    classvar.battle = Battle(enemy)
    classvar.battle.storypenalty = storypenalty
    classvar.battle.reset_time()


class Speak():

    def __init__(self, pic, dialogue, side = None, bottomp = True, options = [], special_battle = "none"):
        self.pic = pic

        # dialogue is a list of strings, one per line
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

        self.state = "talking"

        # options is a list of text for buttons to be displayed at the end of the speak
        self.options = options
        self.choicebuttons = None
        if len(self.options)>0:
            self.choicebuttons = ChoiceButtons(self.options,
                                               variables.height- variables.textsize - variables.height/20,
                                               variables.textsize)
            
        self.special_battle = special_battle
        self.special_battle_story_penalty = None

    def reset(self):
        self.line = 0
        self.state = "talking"

    def wraplines(self):
        index = 0
        while index < len(self.dialogue):
            linedrawn = self.linepic(index)
            if linedrawn.get_width() > variables.width:
                cutpoint = int(len(self.dialogue[index])/2)
                self.dialogue.insert(index+1, self.dialogue[index][cutpoint:])
                self.dialogue[index] = self.dialogue[index][:cutpoint] + "-"
            else:
                index += 1
    
    def linepic(self, index):
        return getTextPic(self.dialogue[index], textsize, variables.WHITE)

    def draw(self):
        if not self.dialogue_initializedp:
            self.initialize_dialogue()
        
        yoffset = 0
        if not self.bottomp:
            yoffset = -variables.height + variables.textbox_height
        #text
        line1 = self.linepic(0)
                                
        line_height = line1.get_height()
        h = variables.height
        w = variables.width
        b = h-variables.textbox_height
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b+yoffset, w, variables.textbox_height])
        numoflines = variables.lines_in_screen
        if numoflines > len(self.dialogue):
            numoflines = len(self.dialogue)
        for x in range(0, numoflines):
            line = self.linepic(x+self.line)
            variables.screen.blit(line, [w/2 - line.get_width()/2, b+(line_height*x)+yoffset])

        if self.line < len(self.dialogue) - variables.lines_in_screen:
            arrowpic = getpic("downarrow", displayscale*2)
        else:
            arrowpic = getpic("rightarrow", displayscale*2)
        variables.screen.blit(arrowpic,
                              [variables.width-2*displayscale*2-arrowpic.get_width(),
                               variables.height-2*displayscale*2-arrowpic.get_height()])

        if self.state == "choosing":
            self.choicebuttons.draw()

    def keypress(self, key):
        choice = None
        if self.line < len(self.dialogue) - variables.lines_in_screen:
            self.line += 1
            return "talking"
        # if there is a choice to be made
        elif self.choicebuttons != None:
            if self.state == "talking":
                self.state = "choosing"
            elif self.state == "choosing":
                if key in variables.settings.leftkeys:
                    self.choicebuttons.previousoption()
                elif key in variables.settings.rightkeys:
                    self.choicebuttons.nextoption()
                elif key in variables.settings.enterkeys:
                    choice = self.choicebuttons.getoption()
                    self.state = "done"
            
        # if there is a specialexitkey, only exit if it is pressed
        elif self.specialexitkeys != None:
            if key in self.specialexitkeys:
                self.state = "done"
        elif key in variables.settings.enterkeys:
            self.state = "done"
        
        returnstate = self.state
        
        if self.state == "done":
            if choice in [None, "y", "yes"]:
                if self.special_battle != "none":
                    initiatebattle(self.special_battle, self.special_battle_story_penalty)
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
