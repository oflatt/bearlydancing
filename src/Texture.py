# This class functions as a data holder for the random texturization module. It defines how the texture is added

class Texture():

    def __init__(self, color, initialchance, xchance, ychance, stopcolors = [], acceptedcolors = None):
        # these handle whether or not points are added after the initial in any of these directions
        self.addupq = False
        self.adddownq = True
        self.addleftq = True
        self.addrightq = True
        # color of the texture added
        self.color = color

        # chance to add color at one pixel and spread
        self.initialchance = initialchance

        # chance to add the color when the x pos is different from the first point
        self.xchance = xchance

        # chance to add the color when the y pos is different
        self.ychance = ychance

        # distruibution for the next pixel
        # can be uniform or geometric
        self.distruibution = "uniform"

        # if true it only picks one of the directions to add out of the ones picked
        self.pickonedirp = False

        # chance for the new point moving the x direction to be invisible, not colored
        self.xinvisiblechance = 0
        self.yinvisiblechance = 0

        # colors not to draw on
        self.stopcolors = stopcolors

        # if acceptedcolors is a list, the color to paint on must be in it
        self.acceptedcolors = acceptedcolors

        # if backtrack mode is off, it will not return back in the direction of the first point
        self.backtrackmodeonq = False

        # if bounds are none, it defaults to using the entire surface, x y width height
        self.bounds = [None, None, None, None]

        # by default set to the bounds, they define the area of pixels to be drawn on
        # the bounds that pixels will have a chance to initiate the texture
        self.texturingbounds = [None, None, None, None]

        # per pixel, vary the colors by this much
        self.redvariancefactor = 0
        self.greenvariancefactor = 0
        self.bluevariancefactor = 0
