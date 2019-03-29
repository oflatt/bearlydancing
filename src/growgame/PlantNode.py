from typing import List, Tuple

from DestructiveFrozenClass import DestructiveFrozenClass

from .PlantShape import PlantShape


class PlantNode(DestructiveFrozenClass):

    def __init__(self, plantshapelist, repeatnumcircle, anglespace, children = [], anchor = (0, 0)):
        
        # a list of PlantShape to make one petal/leaf
        self.plantshapelist : List[PlantShape] = plantshapelist

        # where in the plantshapelist the base of the shape is
        self.anchor : Tuple[float, float] = anchor

        # child PlantNodes
        self.children = children

        # proportion of the angle that spacing can vary
        self.anglevariance = 0.08
        
        # average spacing between plantshapes, in radians
        self.anglespace = anglespace

        # offset the angle in a random direction, makes things droop down
        # angle offset is relative to the angle of the parent node
        self.angleoffset = 0
        
        
        # corresponds to number of petals/branches to make that are identical, in a circle at the same spot
        self.repeatnumcircle = repeatnumcircle

        # corresponds to how many petals/branches to make at different spots
        # example: repeatnumseparate of 3 and repeatnumcircle of 5 would be three groups of 5 petals
        self.repeatnumseparate = 1

        # stretching and shifting
        self.shiftchance = 0.1
        # max  percent of height that can be added on
        self.heightvariance = 0.1
        self.widthvariance = 0.1

        # what percent of the plant you can branch from
        self.brancharea = 0.05

                
        self._freeze()

