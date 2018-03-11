import variables, classvar
from pygame import Rect
from initiatestate import initiatebattle
from graphics import getpicbywidth
from FrozenClass import FrozenClass

class Conversation(FrozenClass):

    def __init__(self, name, speaks, speaksafter=None, switchtheserocks=None):
        # this is the name of the conversation to identify it using currentconversation
        # they have to be unique
        self.name = name
        if name in variables.conversationnames:
            print("-----------------------------------")
            print("Error: duplicate conversation names")
            print("-----------------------------------")
        if not type(name) == str:
            print("-----------------------------------")
            print("Error: got non-string conversation name " + str(name))
            print("-----------------------------------")
        variables.conversationnames.append(name)
        
        # none or an enemy object to encounter after the conversation
        self.special_battle = "none"

        self.progress = 0
        self.timesexited = 0
        
        # a list of Speak
        self.speaks = speaks
        
        # a list of lists of Speak for after the first time they are talked to
        if speaksafter != None:
            if type(speaksafter[0]) == list:
                self.speaksafter = speaksafter
            else:
                self.speaksafter = [speaksafter]
        else:
            self.speaksafter = None

        # a string of a name of a rock to switch the animation of at the beginning of the conversation
        if type(switchtheserocks) == str:
            self.switchtheserocks = [switchtheserocks]
        else:
            self.switchtheserocks = switchtheserocks
        # string of a name of a rock to unhide after the end of the conversation
        self.unhidethisrock = None

        # a list of eventrequirements to check for if the conversation is activated
        self.eventrequirements = []
        # a string of the storyevent that the conversation is
        self.storyevent = None
        
        self.area = [0, 0, 0, 0]  # x, y, width, height in a list (a Rect)
        self.isbutton = True  # true if you have to hit a button to enter
        self.showbutton = True

        self.exitteleport = ["same", "same"]
        self.updatescreenp = False
        
        self._freeze()


    def draw(self):
        if len(self.speaks) > 0:
            # draws text
            self.speaks[self.progress].draw()

            # draw picture
            currentpic = getpicbywidth(self.speaks[self.progress].pic, variables.getphotosize())
            w = currentpic.get_width()
            h = currentpic.get_height()
            b = variables.height - variables.gettextboxheight()
            side = self.speaks[self.progress].side
            
            if (self.progress % 2 == 0 or side == 'l' or side == 'left') and side != 'right':
                xpos = 0
            else:
                xpos = variables.width - w
                
            ypos = b - h
            if not self.speaks[self.progress].bottomp:
                ypos = variables.gettextboxheight()
            variables.screen.blit(currentpic, [xpos, ypos])
            if self.updatescreenp:
                self.updatescreen()


    def updatescreen(self):
        if not len(self.speaks) == 0:
            variables.dirtyrects = [Rect(0,0, variables.width, variables.height)]

    #returns None or the name of a rock to change the animation of
    def keypress(self, key):
        self.updatescreenp = True
        
        if not self.speaks[self.progress].releaseexit:
            self.keyevent(key)

    def keyevent(self, key):
        if len(self.speaks) > 0:
            r = self.speaks[self.progress].keypress(key)
            if r == "done":
                if self.progress < len(self.speaks) - 1:
                    self.progress += 1
                else:
                    if self.speaks[self.progress].specialexitkeys != None:
                        if self.speaks[self.progress].releaseexit:
                            classvar.battle.onrelease(key)
                        else:
                            classvar.battle.onkey(key)
                    self.exit_conversation()

    def keyrelease(self, key):
        if self.speaks[self.progress].releaseexit:
            self.keyevent(key)

    def exit_conversation(self):
        self.updatescreen()
        
        if self.special_battle == "none":
            self.progress = 0
            if variables.settings.backgroundstate == "world":
                variables.settings.state = "world"
            else:
                variables.settings.state = variables.settings.backgroundstate
                classvar.battle.unpause()
        else:
            initiatebattle(self.special_battle)

        self.timesexited += 1
        self.progress = 0
        if self.speaksafter != None and self.timesexited <= len(self.speaksafter):
            self.speaks = self.speaksafter[self.timesexited-1]
        if self.exitteleport != ["same", "same"]:
            classvar.player.teleport(self.exitteleport[0], self.exitteleport[1])

    def scale_by_offset(self, scale):
        s = scale
        self.area = [self.area[0] * s, self.area[1] * s, self.area[2] * s, self.area[3] * s]

    # check all story requirements
    def activatedp(self):
        ap = True
        for e in self.eventrequirements:
            if not e.check():
                ap = False
                break
        return ap
