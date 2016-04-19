#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, graphics

class Conversation():
    area = [0, 0, 0, 0] #x, y, width, height in a list (a Rect)
    isbutton = True #true if you have to hit a button to enter
    progress = 0
    part_of_story = "none"

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
                self.progress = 0
                variables.state = "world"

    def scale_by_offset(self):
        s = variables.scaleoffset
        self.area = [self.area[0]*s, self.area[1]*s, self.area[2]*s, self.area[3]*s]