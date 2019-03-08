import math

from DestructiveFrozenClass import DestructiveFrozenClass


from .PlantNode import PlantNode
from .PlantShape import PlantShape

class ShopPlant(DestructiveFrozenClass):

    def __init__(self, name, headnode, cost):
        self.name = name
        self.headnode = headnode
        self.cost = cost
        self._freeze()

shopplants = []

def getplantbyname(name):
    for p in shopplants:
        if p.name == name:
            return p
    raise Exception("No shopplant with name " + str(name))


def addshopplant(shopplant):
    shopplants.append(shopplant)


bigstem_list = [(0,0)]
for x in range(20):
    bigstem_list.append((x, 0.25))
bigstem_plantshape = PlantShape(bigstem_list, (0, 200, 0), (0, 120, 0))

def add_starter():
    # make the starter flower
    petal_list = [(0, 0)]
    petal_numofpoints = 13
    for x in range(petal_numofpoints):
        petal_list.append((x, 4*math.sin(x/petal_numofpoints * math.pi)))


    petal_shape = PlantShape(petal_list, (0, 0, 200), (0, 0, 120))
    petalnode = PlantNode([petal_shape], 5, (0, 0), math.pi*2 / 5)
    starter_flower = PlantNode([bigstem_plantshape], 1, (0, 0), math.pi/10, children = [petalnode])

    
    addshopplant(ShopPlant("blue flower", starter_flower, 0))


def add_rose():
    petal_list = [(0, 0)]
    petal_numofpoints = 13
    
    for x in range(petal_numofpoints):
        petal_list.append((x, 4*math.sin((1-(x**1.5/petal_numofpoints**1.5)) * math.pi)))

    petal_shape = PlantShape(petal_list, (120, 0, 0), (180, 0, 0))
    petalnode = PlantNode([petal_shape], 3, (0, 0), math.pi/20)
    petalnode = petalnode.destructiveset("anglevariance", 3)
    petalnode = petalnode.destructiveset("heightvariance", 0.75)
    
    rose = PlantNode([bigstem_plantshape], 1, (0, 0), math.pi/10, children = [petalnode])

    addshopplant(ShopPlant("rose", rose, 20))
        

add_starter()
add_rose()
