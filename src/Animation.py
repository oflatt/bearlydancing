
from pygame import Rect

import variables
from graphics import getpicbyheight

class Animation():

    # surfacelist means pics is a list of surfaces- not a list of strings with which to use with GR in graphics
    def __init__(self, picnames, framerate, loopp = True, surfacelist = False, offsetlist = None):
        if not surfacelist:
            if len(picnames):
                if type(picnames[0]) != str and type(picnames[0]) != Animation:
                    raise Exception("Non-string picnames for Animation with surfacelist = False")
                
        # list of names of GR images
        self.pics = picnames
        # milliseconds per frame
        self.framerate = framerate
        self.beginning_time = 0
        self.loopp = loopp
        self.updatealwaysbattle = False
        self.relativeframerate = False
        self.offsetlist = offsetlist

    def current_frame(self, outerframerate = None):
        at = variables.settings.current_time-self.beginning_time
        
        framenum = self.framenum(outerframerate)
        f = self.framerate
        if outerframerate != None and self.relativeframerate:
            f = outerframerate*self.framerate
            
        if type(self.pics[framenum]) == Animation:
            # set the beginning time to the beginning of this animation's frame
            self.pics[framenum].beginning_time = variables.settings.current_time - (at % f)
            return self.pics[framenum].current_frame(self.framerate)
        else:
            return self.pics[framenum]

    ### The following three functions are used as an interface in conjuction with MultiPartAnimation. MultiPartAnimation has no current_frame function
        
    # draws but does not update the screen
    def draw_topright(self, screen, height):
        epic = getpicbyheight(self.current_frame(), height)
        screen.blit(epic, [variables.width - epic.get_width(), 0])

    def update_topright(self, height):
        epic = getpicbyheight(self.current_frame(), height)
        variables.dirtyrects.append(Rect(variables.width-epic.get_width(), 0, epic.get_width(), epic.get_height()))

    def pic_width(self, height):
        epic = getpicbyheight(self.current_frame(), height)
        return epic.get_width()

    def framenum(self, outerframerate):
        f = self.framerate
        if outerframerate != None and self.relativeframerate:
            f = outerframerate*self.framerate
        at = variables.settings.current_time-self.beginning_time
        
        if at>f*len(self.pics):
            if not self.loopp:
                return -1

        return int(at/f) % len(self.pics)
                
    
    def current_offset(self, outerframerate = None):
        if self.offsetlist == None:
            return (0,0)
        at = variables.settings.current_time-self.beginning_time
        return self.offsetlist[int(at/self.framerate)%len(self.offsetlist)]

    def reset(self):
        self.beginning_time = variables.settings.current_time
