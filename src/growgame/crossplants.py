import random

from .Plant import Plant
from .PlantNode import PlantNode
from .PlantShape import PlantShape

combinenodeschance = 0.5
scalenumberchance = 0.2


def combinechildren(nodes):
    alllists = []
    averagesize = 0
    for n in nodes:
        alllists.append(getattr(n, "children"))
        averagesize += len(getattr(n, "children"))
    averagesize = averagesize/len(alllists)
    averagesize = averagesize + random.uniform(0, averagesize/2)

    def randnode():
        return random.choice(random.choice(alllists))
    
    newattr = []
    for i in range(int(averagesize)):
        if random.random() < 0.5:
            newattr.append(crossnodes([randnode(), randnode()]))
        else:
            newattr.append(randnode())
    return newattr

def combineshapes(nodes):
    alllists = []
    averagesize = 0
    for n in nodes:
        alllists.append(getattr(n, "plantshapelist"))
        averagesize += len(getattr(n, "plantshapelist"))
    averagesize = averagesize/len(alllists)
    averagesize = averagesize + random.uniform(0, averagesize/2)

    def randshape():
        return random.choice(random.choice(alllists))

    newattr = []
    for i in range(max(1, int(averagesize))):
        shapes = (randshape(), randshape())
        newshape = PlantShape(random.choice(shapes).polygonlist, random.choice(shapes).fillcolor, random.choice(shapes).outlinecolor, random.choice(shapes).textures, completelistp = True)
        newattr.append(newshape)
    return newattr
    

def crossnodes(nodes):
    def randnode():
        return random.choice(nodes)

    # make a fresh plant node
    pnode = PlantNode([], 0, 0)

    attributes = dir(object.__getattribute__(nodes[0], "item"))

    # pick randomly in the attributes
    for attrkey in attributes:
        if attrkey[0] == '_':
            pass
        else:
            attr = getattr(randnode(), attrkey)
            newattr = None

            if attrkey == "children":
                newattr = combinechildren(nodes)
            elif attrkey == "plantshapelist":
                newattr = combineshapes(nodes)
            elif type(attr) == float or type(attr) == int:
                if random.random() < 0.2:
                    newattr = attr*random.uniform(0.5, 1.5)*random.choice((-1, 1))
                    if type(attr) == int:
                        newattr = int(attr)
                else:
                    newattr = attr
            else:
                newattr = attr
            
            pnode = pnode.destructiveset(attrkey, newattr)
    
    
    return pnode

def crossplants(plant1, plant2):
    return Plant(crossnodes([plant1.headnode, plant2.headnode]))
