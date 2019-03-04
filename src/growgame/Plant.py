from DestructiveFrozenClass import DestructiveFrozenClass


from graphics import flowerpot, getpic

potpic = flowerpot(20)

class Plant(DestructiveFrozenClass):

    def __init__(self, pic):
        self.pic = pic
        self._freeze()

    def draw(self, time, settings, screen, scale):
        screen.blit(getpic(potpic, scale), (0,0))
