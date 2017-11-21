#Oliver Flatt
import variables

class Animation():
    beginning_time = 0

    def __init__(self, pics, framerate):
        self.pics = pics
        # milliseconds per frame
        self.framerate = framerate

    def current_frame(self):
        at = variables.settings.current_time-self.beginning_time
        framenum = int(at/self.framerate) % len(self.pics) - 1
        return self.pics[framenum]

    def reset(self):
        self.beginning_time = variables.settings.current_time
