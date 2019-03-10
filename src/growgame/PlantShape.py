from DestructiveFrozenClass import DestructiveFrozenClass


# corresponds to a part of a single petal/branch
# multiple of these layer to make a petal
class PlantShape(DestructiveFrozenClass):

    def __init__(self, halfpolygonlist, fillcolor, outlinecolor, textures = []):
        # half polygon list is a list that starts at 0, 0 and goes to the right
        # then the half is flipped to make the other side
        self.polygonlist = halfpolygonlist.copy()

        for p in reversed(halfpolygonlist):
            self.polygonlist.append((p[0], -p[1]))

        
        # if either of these is None, then the outline or fill is not drawn
        self.fillcolor = fillcolor
        self.outlinecolor = outlinecolor

        # Texture object- if None no texture is applied
        self.textures = textures
