import math

from DestructiveFrozenClass import DestructiveFrozenClass
from graphics import flowerpot, getpic, makeplant


from .PlantNode import PlantNode
from .PlantShape import PlantShape
from .drawplant import drawplant

potpic = flowerpot(20)
stem_list = [(0,0)]
for x in range(10):
    stem_list.append((x, 0.5))
stem_plant_shape = PlantShape(stem_list, (0, 200, 0), (0, 120, 0))
basicFlowerHeadNode = PlantNode([stem_plant_shape], 1, (0, 0), math.pi/10)

class Plant(DestructiveFrozenClass):

    def __init__(self, pic):
        self.headNode = basicFlowerHeadNode
        
        self.pic = makeplant(self.headNode)
        self._freeze()

    def draw(self, time, settings, screen, scale):
        screen.blit(getpic(potpic, scale), (0,12*scale))
        screen.blit(getpic(self.pic, scale), (0,0))
