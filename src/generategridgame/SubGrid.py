from pygame import Rect 


from DestructiveFrozenClass import DestructiveFrozenClass

class SubGrid(DestructiveFrozenClass):

    # all measurements in rect are fractions of the screen- with of 1 is one screen width
    def __init__(rect, lavas):

        self.rect = rect
        self.lavas = lavas

        self._freeze()
