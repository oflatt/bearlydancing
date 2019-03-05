from DestructiveFrozenClass import DestructiveFrozenClass


class PlantNode(DestructiveFrozenClass):

    def __init__(self, plantshapelist, repeatnum, anchor, anglespace):

        # a list of PlantShape to make one petal/leaf
        self.plantshapelist = plantshapelist

        # where in the plantshapelist the base of the shape is
        self.anchor = anchor

        # child PlantNodes
        self.children = []

        # average spacing between plantshapes, in radians
        self.anglespace = anglespace
        
        # corresponds to number of petals/branches to make that are identical
        self.repeatnum = repeatnum

        self.shiftchance = 0.15
        
        self._freeze()

