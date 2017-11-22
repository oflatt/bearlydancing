#!/usr/bin/python
# Oliver Flatt works on Classes
import variables, classvar, stathandeling
from Battle import Battle


class Conversation():
    area = [0, 0, 0, 0]  # x, y, width, height in a list (a Rect)
    isbutton = True  # true if you have to hit a button to enter
    progress = 0
    #the number of the story that it is
    part_of_story = "none"
    #list of all the story numbers that it would appear in
    #empty means none
    storyrequirement = []
    special_battle = "none"  # none or an enemy to encounter after the conversation
    timestalkedto = 0
    exitteleport = ["same", "same"]
    speaksafter = None
    switchthisrock = None

    def __init__(self, speaks, speaksafter=None, switchthisrock=None):
        # a list of Speak
        self.speaks = speaks
        
        # a list lists of Speak for after the first time they are talked to
        if speaksafter != None:
            if type(speaksafter) == list:
                self.speaksafter = speaksafter
            else:
                self.speaksafter = [speaksafter]

        # a string of a name of a rock to switch the animation of
        if switchthisrock != None:
            self.switchthisrock = switchthisrock

    def draw(self):
        if len(self.speaks) > 0:
            # draws text
            self.speaks[self.progress].draw()

            # draw picture
            currentpic = self.speaks[self.progress].pic
            w = currentpic.get_width()
            h = currentpic.get_height()
            b = variables.height - variables.textbox_height
            if self.progress % 2 == 0 or self.speaks[self.progress].side == 'l' or self.speaks[
                    self.progress].side == 'left':
                xpos = 0
            else:
                xpos = variables.width - w
            variables.screen.blit(currentpic, [xpos, b - h])

    #returns None or the name of a rock to change the animation of
    def keypress(self, key):
        if len(self.speaks) > 0:
            r = self.speaks[self.progress].keypress(key)
            if r == "done":
                if self.progress < len(self.speaks) - 1:
                    self.progress += 1
                else:
                    self.exit_conversation()

    def exit_conversation(self):
        
        if self.special_battle == "none":
            self.progress = 0
            variables.settings.state = "world"
        else:
            variables.settings.state = "battle"
            classvar.player.change_of_state()
            self.special_battle.health = stathandeling.max_health(self.special_battle.lv)
            classvar.battle = Battle(self.special_battle)

        self.timestalkedto += 1
        if self.speaksafter != None and self.timestalkedto < len(self.speaksafter):
            self.speaks = self.speaksafter[self.timestalkedto]
        if self.exitteleport != ["same", "same"]:
            classvar.player.teleport(self.exitteleport[0], self.exitteleport[1])

    def scale_by_offset(self, scale):
        s = scale
        self.area = [self.area[0] * s, self.area[1] * s, self.area[2] * s, self.area[3] * s]
