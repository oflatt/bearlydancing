from FrozenClass import FrozenClass

class VolumeEnvelope(FrozenClass):

    def __init__(self, timevollist, endoscilationrate, endoscilationvolume):
        # lists of tuples that have a time and a volume in them
        self.timevollist = timevollist
        # period of oscilation of volume at end
        self.endoscilationrate = endoscilationrate
        # how much the volume changes over time at end
        self.endoscilationvolume = endoscilationvolume
