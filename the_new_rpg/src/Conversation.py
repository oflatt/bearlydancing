#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, classvar, stathandeling
from Battle import Battle

class Conversation():
    area = [0, 0, 0, 0] #x, y, width, height in a list (a Rect)
    isbutton = True #true if you have to hit a button to enter
    progress = 0
    part_of_story = "none"
    special_battle = "none" #none or an enemy to encounter after the conversation

    def __init__(self, speaks):
        #a list of Speak
        self.speaks = speaks

    def draw(self):
        #draws text
        self.speaks[self.progress].draw()

        #draw picture
        currentpic = self.speaks[self.progress].pic
        w = currentpic.get_width()
        h = currentpic.get_height()
        b = variables.height-variables.textbox_height
        if self.progress % 2 == 0:
            xpos = 0
        else:
            xpos = variables.width-w
        variables.screen.blit(currentpic, [xpos, b - h])


    def keypress(self, key):
        r = self.speaks[self.progress].keypress(key)
        if r == "done":
            if self.progress < len(self.speaks)-1:
                self.progress += 1
            else:
                self.exit_conversation()

    def exit_conversation(self):
        if self.special_battle == "none":
            self.progress = 0
            variables.state = "world"
        else:
            variables.state = "battle"
            classvar.player.change_of_state()
            self.special_battle.health = stathandeling.max_health(self.special_battle.lv)
            classvar.battle = Battle(self.special_battle)

    def scale_by_offset(self):
        s = variables.scaleoffset
        self.area = [self.area[0]*s, self.area[1]*s, self.area[2]*s, self.area[3]*s]