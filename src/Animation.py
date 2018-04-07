#Oliver Flatt
import variables

class Animation():

    def __init__(self, picnames, framerate, loopp = True):
        if len(picnames):
            if type(picnames[0]) != str and type(picnames[0]) != Animation:
                print("got a non-string or non-animation list of pics for an Animation")
        # list of names of GR images
        self.pics = picnames
        # milliseconds per frame
        self.framerate = framerate
        self.beginning_time = 0
        self.loopp = loopp
        self.updatealwaysbattle = False

    def current_frame(self):
        at = variables.settings.current_time-self.beginning_time
        framenum = int(at/self.framerate) % len(self.pics)
        if at>self.framerate:
            if not self.loopp:
                framenum = -1
        if type(self.pics[framenum]) == Animation:
            # set the beginning time to the beginning of this animation's frame
            self.pics[framenum].beginning_time = variables.settings.current_time - (at % self.framerate)
            return self.pics[framenum].current_frame()
        else:
            return self.pics[framenum]

    def reset(self):
        self.beginning_time = variables.settings.current_time
