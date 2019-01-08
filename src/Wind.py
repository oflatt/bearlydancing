import random

from FrozenClass import FrozenClass
import variables

class Wind(FrozenClass):

    # creates a new wind object, defaulting it at the left side of the screen.
    def __init__(self):

        self.starttime = variables.settings.current_time

        # speed is measured in pixels per second
        self.speed = random.randint(45, 75)


        self._freeze()

    # returns the position of the wind in pixels
    def windpos(self):
        return int((variables.settings.current_time - self.starttime)/1000 * self.speed)

