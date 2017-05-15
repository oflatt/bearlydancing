# This class functions as a data holder for the random texturization module. It defines how the texture is added

class Texture():
    # these handle whether or not points are added after the initial in any of these directions
    addupq = False
    adddownq = True
    addleftq = True
    addrightq = True

    # if bounds are none, it defaults to using the entire surface
    bounds = [None, None, None, None]

    def __init__(self, color, initialchance, xchance, ychance, stopcolors = []):
        # color of the texture added
        self.color = color

        # chance to add color at one pixel and spread
        self.initialchance = initialchance

        # chance to add the color when the x pos is different from the first point
        self.xchance = xchance

        # chance to add the color when the y pos is different
        self.ychance = ychance

        # colors not to draw on
        self.stopcolors = stopcolors
