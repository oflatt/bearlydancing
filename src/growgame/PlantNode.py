from DestructiveFrozenClass import DestructiveFrozenClass


class PlantNode(DestructiveFrozenClass):

    def __init__(self, plantshapelist, repeatnum, anchor, anglespace, children = []):

        # a list of PlantShape to make one petal/leaf
        self.plantshapelist = plantshapelist

        # where in the plantshapelist the base of the shape is
        self.anchor = anchor

        # child PlantNodes
        self.children = children

        # proportion of the angle that spacing can vary
        self.anglevariance = 0.08
        
        # average spacing between plantshapes, in radians
        self.anglespace = anglespace

        # offset the angle in a random direction, makes things droop down
        self.angleoffset = 0
        
        # corresponds to number of petals/branches to make that are identical
        self.repeatnum = repeatnum

        self.shiftchance = 0.15

        # what percent of the plant you can branch from
        self.brancharea = 0.05

        
        
        self._freeze()

