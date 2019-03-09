import math

from DestructiveFrozenClass import DestructiveFrozenClass
from variables import brighten
from rdraw.pointlist import listarc
from rdraw.Texture import Texture

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


    middlecolor = (241, 252, 63)
    middletexture = Texture(brighten(middlecolor, -50), 0.25, 0.1, 0.1, acceptedcolors = [middlecolor])

    middleradius = 2.5
    middlelist = listarc(-middleradius, 0, middleradius*2, middleradius, 8)
    middleshape = PlantShape(middlelist, middlecolor, brighten(middlecolor, -30))
    middlenode = PlantNode([middleshape], 1, (0, 0), math.pi/20)

    petal_shape = PlantShape(petal_list, (0, 0, 200), (0, 0, 120))
    petalnode = PlantNode([petal_shape], 5, (0, 0), math.pi*2 / 5)
    starter_flower = PlantNode([bigstem_plantshape], 1, (0, 0), math.pi/10, children = [middlenode, petalnode])
    

    
    addshopplant(ShopPlant("blue flower", starter_flower, 0))


def add_rose():
    petal_list = [(0, 0)]
    petal_numofpoints = 13
    
    for x in range(petal_numofpoints):
        petal_list.append((x*0.75, 2*math.sin((1-(x**1.5/petal_numofpoints**1.5)) * math.pi)))

    petal_shape = PlantShape(petal_list, (120, 0, 0), (180, 0, 0))
    petalnode = PlantNode([petal_shape], 4, (0, 0), math.pi/8)
    petalnode = petalnode.destructiveset("anglevariance", 0.3)
    petalnode = petalnode.destructiveset("heightvariance", 0.2)
    petalnode = petalnode.destructiveset("widthvariance", 1)

    
    innerpetal_list = [(0, 0)]
    innerpetal_numofpoints = 13
    
    for x in range(innerpetal_numofpoints):
        innerpetal_list.append((x*0.75, 1.5*math.sin((1-(x**1.5/innerpetal_numofpoints**1.5)) * math.pi)))

    innerpetal_shape = PlantShape(innerpetal_list, (100, 0, 0), (120, 0, 0))
    innerpetalnode = PlantNode([innerpetal_shape], 4, (0, 0), 0)
    innerpetalnode = innerpetalnode.destructiveset("anglevariance", 0)
    innerpetalnode = innerpetalnode.destructiveset("heightvariance", 0.4)

    spikes_list = [(0, 0.5), (2, 0)]
    spikes_shape = PlantShape(spikes_list, (50, 70, 50), brighten((50, 85, 50), 20))
    spikes_node = PlantNode([spikes_shape], 1, (0, 0), math.pi)
    spikes_node = spikes_node.destructiveset("angleoffset", math.pi/2)
    spikes_node = spikes_node.destructiveset("repeatnumseparate", 4)
    spikes_node = spikes_node.destructiveset("brancharea", 1)
    
    rose = PlantNode([bigstem_plantshape], 1, (0, 0), math.pi/10, children = [petalnode, innerpetalnode, spikes_node])

    addshopplant(ShopPlant("rose", rose, 20))


add_starter()
#add_rose()
