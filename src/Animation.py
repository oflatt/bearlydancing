#Oliver Flatt
import variables

class Animation():
    beginning_time = 0

    def __init__(self, picnames, framerate):
        if len(picnames):
            if type(picnames[0]) != str:
                print("got a non-string list of pics for an Animation")
        # list of names of GR images
        self.pics = picnames
        # milliseconds per frame
        self.framerate = framerate

    def current_frame(self):
        at = variables.settings.current_time-self.beginning_time
        framenum = int(at/self.framerate) % len(self.pics) - 1
        return self.pics[framenum]

    def reset(self):
        self.beginning_time = variables.settings.current_time
