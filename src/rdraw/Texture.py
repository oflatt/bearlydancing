# This class functions as a data holder for the random texturization module. It defines how the texture is added
from FrozenClass import FrozenClass

class Texture(FrozenClass):

    def __init__(self, color, initialchance, xchance, ychance, stopcolors = [], acceptedcolors = None, verticalcolorchange = (0,0,0)):
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

        # per pixel, vary the colors by this much (on either side, so a variance of 5 is + or - 5)
        self.redvariancefactor = 0
        self.greenvariancefactor = 0
        self.bluevariancefactor = 0
        
        self.redvarianceperspawn = 2
        self.greenvarianceperspawn = 2
        self.bluevarianceperspawn = 2

        # change the colors by this every time you move vertically
        # ex: (10, 10, 10) would make the color brighter as you move down
        self.verticalcolorchange = verticalcolorchange
        
        self._freeze()
