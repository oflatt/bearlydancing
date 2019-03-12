from DestructiveFrozenClass import DestructiveFrozenClass


# corresponds to a part of a single petal/branch
# multiple of these layer to make a petal
class PlantShape(DestructiveFrozenClass):

    def __init__(self, halfpolygonlist, fillcolor, outlinecolor, textures = [], completelistp = False):
        # half polygon list is a list that starts at 0, 0 and goes to the right
        # then the half is flipped to make the other side
        
        # polygonlist must be a list of even numbered points that makes a loop, and the second half must have the same x positions as the first half
        # the points must go clockwise

        
        if not completelistp:
            self.polygonlist = halfpolygonlist.copy()

            for p in reversed(halfpolygonlist):
                self.polygonlist.append((p[0], -p[1]))
        else:
            self.polygonlist = halfpolygonlist
            if not len(self.polygonlist) % 2 == 0:
                raise Exception("polygon list length must be even")
            for i in range(int(len(self.polygonlist)/2)):
                if not self.polygonlist[i][0] == self.polygonlist[-i][0]:
                    raise Exception("polygon list x positions in second half must correspond to x positions in first half")

        

        
        # if either of these is None, then the outline or fill is not drawn
        self.fillcolor = fillcolor
        self.outlinecolor = outlinecolor

        # Texture object- if None no texture is applied
        self.textures = textures
