#!/usr/bin/python
# Oliver Flatt works on Classes
import variables, classvar
from Speak import initiatebattle
from graphics import getpicbywidth


class Conversation():

    def __init__(self, speaks, speaksafter=None, switchthisrock=None):
        # none or an enemy object to encounter after the conversation
        self.special_battle = "none"
        
        self.special_battle_story_penalty = None
        self.progress = 0
        self.timestalkedto = 0
        # the number of times you can activate the conversation
        self.talkedtolimit = None
        
        # a list of Speak
        self.speaks = speaks
        #list of all the story numbers that it would appear in
        self.storyrequirement = []
        
        # a list of lists of Speak for after the first time they are talked to
        if speaksafter != None:
            if type(speaksafter[0]) == list:
                self.speaksafter = speaksafter
            else:
                self.speaksafter = [speaksafter]
        else:
            self.speaksafter = None

        # a string of a name of a rock to switch the animation of at the beginning of the conversation
        self.switchthisrock = switchthisrock
        # string of a name of a rock to unhide after the end of the conversation
        self.unhidethisrock = None

        self.area = [0, 0, 0, 0]  # x, y, width, height in a list (a Rect)
        self.isbutton = True  # true if you have to hit a button to enter
        self.showbutton = True

        # conditions for increasing the story
        # none on both means never
        self.storytimestalkedtolessthan = None
        self.storytimestalkedtogreaterthan = None

        self.exitteleport = ["same", "same"]

    def draw(self):
        if len(self.speaks) > 0:
            # draws text
            self.speaks[self.progress].draw()

            # draw picture
            currentpic = getpicbywidth(self.speaks[self.progress].pic, variables.photo_size)
            w = currentpic.get_width()
            h = currentpic.get_height()
            b = variables.height - variables.textbox_height
            side = self.speaks[self.progress].side
            if (self.progress % 2 == 0 or side == 'l' or side == 'left') and side != 'right':
                xpos = 0
            else:
                xpos = variables.width - w
            ypos = b - h
            if not self.speaks[self.progress].bottomp:
                ypos = variables.textbox_height
            variables.screen.blit(currentpic, [xpos, b - h])

    #returns None or the name of a rock to change the animation of
    def keypress(self, key):
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
        
        if self.special_battle == "none":
            self.progress = 0
            if variables.settings.backgroundstate == "world":
                variables.settings.state = "world"
            else:
                variables.settings.state = variables.settings.backgroundstate
                classvar.battle.unpause()
        else:
            initiatebattle(self.special_battle, self.special_battle_story_penalty)

        self.timestalkedto += 1
        self.progress = 0
        if self.speaksafter != None and self.timestalkedto <= len(self.speaksafter):
            self.speaks = self.speaksafter[self.timestalkedto-1]
        if self.exitteleport != ["same", "same"]:
            classvar.player.teleport(self.exitteleport[0], self.exitteleport[1])

    def scale_by_offset(self, scale):
        s = scale
        self.area = [self.area[0] * s, self.area[1] * s, self.area[2] * s, self.area[3] * s]
