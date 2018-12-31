import math
from FrozenClass import FrozenClass

class VolumeEnvelope(FrozenClass):

    def __init__(self, timevollist, endoscilationrate, endoscilationvolume):
        # lists of tuples that have a time and a volume in them
        self.timevollist = timevollist
        # period of oscilation of volume at end
        self.endoscilationrate = endoscilationrate
        # how much the volume changes over time at end
        self.endoscilationvolume = endoscilationvolume

    # durationplayed is in milliseconds
    def tone_volume(self, durationplayed):
        listplace = 0
        while True:
            if listplace + 1 >= len(self.timevollist):
                break
            elif durationplayed >= self.timevollist[listplace + 1][0]:
                listplace += 1
            else:
                break

        dt = durationplayed - self.timevollist[listplace][0]
        if listplace >= len(self.timevollist)-1:
            volume = self.timevollist[listplace][1]
            timesinceend = durationplayed-self.timevollist[-1][0]
            volume = volume + math.sin(2*math.pi*timesinceend/self.endoscilationrate)*self.endoscilationvolume
        else:
            # move between two list places using a sin wave
            timebetween = (self.timevollist[listplace+1][0]-self.timevollist[listplace][0])
            ydifference = (self.timevollist[listplace+1][1]-self.timevollist[listplace][1])
            initial = self.timevollist[listplace][1]
            volume = initial + ydifference * math.sin(math.pi/2 * dt/timebetween)

        return volume
