import random, copy
from typing import List

from variables import devprint

from .Plant import Plant
from .PlantNode import PlantNode
from .PlantShape import PlantShape

crossnodeschance = 0.2
scalenumberchance = 0.2
crosscolorschance = 0.5
texturematchchance = 0.5

def colorvariation(color):
    def processone(n):
        return min(255, (max(0, n + random.randint(-2, 2)))*random.uniform(1/1.2, 1.2))
        
    return (processone(color[0]),
            processone(color[1]),
            processone(color[2]))

# make the texture from the originalshape work with the new shape
def fix_textures(newshape, originalshape):
    for t in newshape.textures:
        # fix stopcolors
        t.stopcolors = []
        for c in t.stopcolors:
            if c == originalshape.fillcolor:
                t.stopcolors.append(newshape.fillcolor)
            elif c == originalshape.outlinecolor:
                t.stopcolors.append(newshape.outlinecolor)
            else:
                t.stopcolors.append(newshape.outlinecolor)

        # fix stopcolors
        t.stopcolors = []
        for c in t.stopcolors:
            if c == originalshape.fillcolor:
                t.stopcolors.append(newshape.fillcolor)
            elif c == originalshape.outlinecolor:
                t.stopcolors.append(newshape.outlinecolor)
            else:
                t.stopcolors.append(newshape.outlinecolor)

        # fix acceptedcolors
        t.acceptedcolors = []
        for c in t.acceptedcolors:
            if c == originalshape.fillcolor:
                t.acceptedcolors.append(newshape.fillcolor)
            elif c == originalshape.outlinecolor:
                t.acceptedcolors.append(newshape.outlinecolor)
            else:
                t.acceptedcolors.append(newshape.outlinecolor)

        # fix stopcolors
        t.acceptedcolorsspawn = []
        for c in t.acceptedcolorsspawn:
            if c == originalshape.fillcolor:
                t.acceptedcolorsspawn.append(newshape.fillcolor)
            elif c == originalshape.outlinecolor:
                t.acceptedcolorsspawn.append(newshape.outlinecolor)
            else:
                t.acceptedcolorsspawn.append(newshape.outlinecolor)

        # randomly change numbers
        attributes = dir(t)
        for a in attributes:
            if a[0] == "_":
                pass

            if type(getattr(t, a)) == float or type(getattr(t, a)) == int:
                if random.random() < scalenumberchance:
                    setattr(t, a, getattr(t, a) * random.uniform(0.5, 2))


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

    def getrandomcolors():
        randomcolorindex = random.randint(0, len(shapes)-1)
        randomoutlinecolorindex = randomcolorindex
        if random.random() < 0.1:
            randomoutlinecolorindex = random.randint(0, len(shapes)-1)

        return colorvariation(shapes[randomcolorindex].fillcolor), colorvariation(shapes[randomoutlinecolorindex].outlinecolor)

    def randomcombinecolors(c1, c2):
        firstweight = random.uniform(0.25, 0.75)
        # extra chance to make it lopsided
        if random.random() < 0.5:
            firstweight = firstweight / random.uniform(2, 4)
        secondweight = 1-firstweight
        return (int(c1[0]*firstweight+c2[0]*secondweight),
                int(c1[1]*firstweight+c2[1]*secondweight),
                int(c1[2]*firstweight+c2[2]*secondweight))

    newattr = []
    for i in range(max(1, int(averagesize))):
        shapes = (randshape(), randshape())

        randomcolor, randomoutlinecolor = getrandomcolors()

        if random.random() < crosscolorschance:
            secondcolor, secondoutlinecolor = getrandomcolors()
            randomcolor = randomcombinecolors(randomcolor, secondcolor)
            randomoutlinecolor = randomcombinecolors(randomcolor, secondcolor)

        randompolygonlistindex = random.randint(0, len(shapes)-1)
        donernode = nodes[randompolygonlistindex]
        if random.random() < texturematchchance:
            originaltextureshape = shapes[randompolygonlistindex]
        else:
            originaltextureshape = random.choice(shapes)

        randomtextures = copy.deepcopy(originaltextureshape.textures)
        
        newshape = PlantShape(shapes[randompolygonlistindex].polygonlist,
                              randomcolor, randomoutlinecolor,
                              randomtextures, completelistp = True)

        fix_textures(newshape, originaltextureshape)
        
        newattr.append(newshape)
    return newattr, donernode
    

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
                newattr = [] # ignore children because we are only crossing two nodes
            elif attrkey == "plantshapelist":
                newattr, shapedonernode = combineshapes(nodes)
            elif type(attr) == float or type(attr) == int:
                if random.random() < 0.2:
                    newattr = attr*random.uniform(0.5, 2)*random.choice((-1, 1))
                    if type(attr) == int:
                        newattr = int(attr)
                else:
                    newattr = attr
            else:
                newattr = attr
            
            pnode = pnode.destructiveset(attrkey, newattr)

    # hand tuned attributes

    # chance to pick difference nodes for the repeat numbers
    if random.random() < 0.1:
        pnode = pnode.destructiveset("repeatnumseparate", nodes[random.randint(0, len(nodes)-1)].repeatnumseparate)
        pnode = pnode.destructiveset("repeatnumcircle", nodes[random.randint(0, len(nodes)-1)].repeatnumcircle)
    else:
        repeatnumindex = random.randint(0, len(nodes)-1)
        pnode = pnode.destructiveset("repeatnumseparate", nodes[repeatnumindex].repeatnumseparate)
        pnode = pnode.destructiveset("repeatnumcircle", nodes[repeatnumindex].repeatnumcircle)

    # make repeat numbers closer to doner node's
    if random.random() < 0.8:
        donerweight = random.uniform(0.25, 0.75)
        pnode = pnode.destructiveset("repeatnumseparate",
                                     int(pnode.repeatnumseparate*(1-donerweight) + shapedonernode.repeatnumseparate*donerweight))
        pnode = pnode.destructiveset("repeatnumcircle",
                                     int(pnode.repeatnumcircle*(1-donerweight) + shapedonernode.repeatnumcircle*donerweight))
    
    return pnode

def get_plant_layer_list(plant) -> List[List[PlantNode]]:
    l = []
    currentlayer = [plant.headnode]

    while len(currentlayer) > 0:
        nextlayer : List[PlantNode] = []
        for node in currentlayer:
            nextlayer = nextlayer + node.children

        # also make the nodes not have children for the layer list
        for i in range(len(currentlayer)):
            currentlayer[i] = copy.copy(currentlayer[i])
            currentlayer[i] = currentlayer[i].destructiveset("children", [])
            
        l.append(currentlayer)
        currentlayer = nextlayer

    return l

def random_layer_size(layerlists : List[List[List[PlantNode]]], layerindex) -> int:
    total = 0
    number_added_to_total = 0
    for plantlayer in layerlists:
        if layerindex < len(plantlayer):
           total += len(plantlayer[layerindex])
           number_added_to_total += 1

    if total == 0:
        return len(random.choice(random.choice(layerlists)))
    else:
        average = total / number_added_to_total
        return max(1, random.randint(int(average*0.7), int(average*1.3)))


# layerindex refers to which layer is currently being created in the new plant
def random_node_at_layer(layerlists : List[List[PlantNode]], layerindex):
    devprint("random node at layer " + str(layerindex))
    # sort by length
    layerlists = sorted(layerlists, key = len)
    maxlayer = len(layerlists[-1])-1
    
    def random_node_from_layer(layerindex):
        # choose an i such that all the layers on i and over have enough layers
        i = 0
        while len(layerlists[i])-1 < layerindex:
            i += 1
        randomlayerlist = layerlists[random.randint(i, layerindex)]
        # choose a random node in that layer list
        return random.choice(randomlayerlist[layerindex])
    
    def random_node():
        # most of the time pick from one of the same layer in the else
        random_layer = layerindex

        if layerindex > maxlayer:
            random_layer = random.randint(0, maxlayer)
        elif random.random() < 0.3: # chance for after index
            random_layer = random.randint(layerindex, maxlayer)
        elif random.random() < 0.05:
            random_layer = random.randint(0, layerindex)
        return random_node_from_layer(random_layer)

    # chance to cross nodes
    if random.random() < crossnodeschance:
        devprint("crossing nodes")
        return crossnodes([random_node(), random_node()])
    else:
        return copy.deepcopy(random_node())


# destroys one layerlist, returning a plant head node
def layer_list_to_node(layerlist : List[List[PlantNode]]):
    # this first layer list should always have only one node in it
    if not len(layerlist[0]) == 1:
        raise Exception("Got layer list where first list did not just have one item in it")
    
    # iterate through all layers but the first one
    for i in range(len(layerlist)-1, 0, -1):
        layerbefore : List[PlantNode] = layerlist[i-1]
        thislayer = layerlist[i]
        for node in thislayer:
            # add node to random node in layer before
            random.choice(layerbefore).children.append(node)
    return layerlist[0][0]


def crossplants(plant1, plant2):
    plant1_layer_list = get_plant_layer_list(plant1)
    plant2_layer_list = get_plant_layer_list(plant2)
    smallerlength = min(len(plant1_layer_list), len(plant2_layer_list))
    biggerlength = max(len(plant1_layer_list), len(plant2_layer_list))

    # pick some number between their layers and also have a chance to add 1
    newplant_num_of_layers = random.randint(smallerlength, biggerlength)
    if random.random() < 0.2:
        newplant_num_of_layers += 1 

    # add layers
    layer_list : List[List[PlantNode]] = [] # the new plant's layer list
    for i in range(newplant_num_of_layers):
        layer_size = random_layer_size([plant1_layer_list, plant2_layer_list], i)
        new_layer = []
        for not_used in range(layer_size):
            new_layer.append(random_node_at_layer((plant1_layer_list, plant2_layer_list), i))
        layer_list.append(new_layer)

    
    print(layer_list)
    return Plant(layer_list_to_node(layer_list))
