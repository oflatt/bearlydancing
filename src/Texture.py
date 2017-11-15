# This class functions as a data holder for the random texturization module. It defines how the texture is added

class Texture():
    # these handle whether or not points are added after the initial in any of these directions
    addupq = False
    adddownq = True
    addleftq = True
    addrightq = True

    # if bounds are none, it defaults to using the entire surface, x y width height
    bounds = [None, None, None, None]

    # by default set to the bounds, they define the area of pixels to be drawn on
    texturingbounds = [None, None, None, None]

    # chance for the new point moving the x direction to be invisible, not colored
    xinvisiblechance = 0
    yinvisiblechance = 0

    # if backtrack mode is off, it will not return back in the direction of the first point
    backtrackmodeonq = False

    def __init__(self, color, initialchance, xchance, ychance, stopcolors = [], acceptedcolors = None):
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

        # if acceptedcolors is a list, the color to paint on must be in it
        self.acceptedcolors = acceptedcolors
