import random, copy
from typing import List

from colormath.color_objects import sRGBColor, HSLColor
from colormath import color_conversions


from variables import devprint

from .Plant import Plant
from .PlantNode import PlantNode
from .PlantShape import PlantShape


# chance that when adding nodes to a layer, a node from a layer after that node is picked
def picknodeafterlayerchance(currentlayer):
    return 0.05 + max(currentlayer*0.2, 0.25)

# chance that when adding nodes to a layer, a node from an earlier layer in the original plants is added
def picknodebeforelayerchance(currentlayer):
    return 0.03

# chance when adding nodes to cross two nodes together
crossnodeschance = 0.4


# chance that a shape retains it's color when being combined with another shape
colormatchdonershapechance = 0.6
# chance that the texture of a plant shape follows it when being crossed with another plant shape
texturematchchance = 0.5

# chance that an attribute of a node gets scaled randomly
scalenumberchance = 0.2

# chance to mix colors instead of picking one color
crosscolorschance = 0.7

# chance that a shape is picked from the primary node when mixing two nodes together
donernodechance = 0.8

def colorvariation(color):
    def processone(n):
        return min(255, (max(0, n + random.randint(-2, 2)))*random.uniform(1/1.2, 1.2))
        
    return (processone(color[0]),
            processone(color[1]),
            processone(color[2]))

def circle_ave(a0, a1, circlerange):
    r = (a0+a1)/2., ((a0+a1+circlerange)/2.)%circlerange
    if min(abs(a1-r[0]), abs(a0-r[0])) < min(abs(a0-r[1]), abs(a1-r[1])):
        return r[0]
    else:
        return r[1]

def randomcombinecolors(c1, c2):
    devprint("combine colors")
    weight1 = random.uniform(0, 1)
    return combinecolors(c1, c2, weight1)

def combinecolors(c1, c2, firstweight):
    firstweight = random.uniform(0.25, 0.75)
    # extra chance to make it lopsided
    if random.random() < 0.5:
        firstweight = firstweight / random.uniform(2, 4)
        
    secondweight = 1-firstweight

    c = sRGBColor(c1[0], c1[1], c1[2], is_upscaled = True)
    c2 = sRGBColor(c2[0], c2[1], c2[2], is_upscaled = True)
    
    hsl1 = color_conversions.convert_color(c, HSLColor)
    hsl2 = color_conversions.convert_color(c2, HSLColor)
    hue1 = hsl1.hsl_h
    hue2 = hsl2.hsl_h

    # jank recombination of hue
    # make hue2 the greater one
    if hue2 > hue1:
        temp = hue1
        hue1 = hue2
        hue2 = temp

    # shrink green region to make recombination work- green is from 75 to 150
        
    recombinecount = 0
    if hue1 > 75:
        subtract = min((hue1-75), 25)
        hue1 = hue1 - subtract
        recombinecount += 1
    if hue2 > 75:
        subtract = min((hue2-75), 25)
        hue2 = hue2 - subtract
        recombinecount += 1
        
    new_hue = circle_ave(hue1, hue2, circlerange = 360-25)
    # add both if it was found on the greater side of the circle
    if new_hue > hue2 and recombinecount > 0:
        recombinecount = 2
    
    # convert back with green
    if new_hue > 75:
        new_hue = new_hue + (min(new_hue-75, 25)/2) * recombinecount
    
    new_hsl = HSLColor(new_hue,
                       hsl1.hsl_s*firstweight+hsl2.hsl_s*(1-firstweight),
                       hsl1.hsl_l*firstweight+hsl2.hsl_l*(1-firstweight))
    rgb = color_conversions.convert_color(new_hsl, sRGBColor)
    pygame_rgb = (int(rgb.rgb_r * 255), int(rgb.rgb_g * 255), int(rgb.rgb_b * 255))
    
    return pygame_rgb

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

# when combining two plant nodes, combine all their shapes
def combineshapes(nodes):
    alllists = []
    averagesize = 0
    for n in nodes:
        alllists.append(getattr(n, "plantshapelist"))
        averagesize += len(getattr(n, "plantshapelist"))
    averagesize = averagesize/len(alllists)
    averagesize = averagesize + random.uniform(0, averagesize/2)
    # primary node in combining
    donernode = random.choice(nodes)
    donerlist = copy.copy(donernode.plantshapelist)
    

    def randshape():
        if len(donerlist) > 0 and random.random() < donernodechance:
            return donerlist.pop(random.randint(0, len(donerlist)-1))
        else:                
            return random.choice(random.choice(alllists))

    def getrandomcolors(shapes):
        randomcolorindex = random.randint(0, len(shapes)-1)
        if random.random() < colormatchdonershapechance:
            randomcolorindex = 0
        randomoutlinecolorindex = randomcolorindex
        if random.random() < 0.1:
            randomoutlinecolorindex = random.randint(0, len(shapes)-1)

        return colorvariation(shapes[randomcolorindex].fillcolor), colorvariation(shapes[randomoutlinecolorindex].outlinecolor)

    newattr = []
    for i in range(max(1, int(averagesize))):
        shapes = (randshape(), randshape())
        # primary shape in combining two shapes
        donershape = shapes[0]

        randomcolor, randomoutlinecolor = getrandomcolors(shapes)

        if random.random() < crosscolorschance:
            secondcolor, secondoutlinecolor = getrandomcolors(shapes)
            randomcolor = randomcombinecolors(randomcolor, secondcolor)
            randomoutlinecolor = randomcombinecolors(randomcolor, secondcolor)

        
        if random.random() < texturematchchance:
            originaltextureshape = donershape
        else:
            originaltextureshape = random.choice(shapes)

        randomtextures = copy.deepcopy(originaltextureshape.textures)
        
        newshape = PlantShape(donershape.polygonlist,
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

    #### hand tuned attributes


    # chance to pick difference nodes for the repeat numbers
    if random.random() < 0.1:
        pnode = pnode.destructiveset("repeatnumseparate", nodes[random.randint(0, len(nodes)-1)].repeatnumseparate)
        pnode = pnode.destructiveset("repeatnumcircle", nodes[random.randint(0, len(nodes)-1)].repeatnumcircle)
    else:
        repeatnumindex = random.randint(0, len(nodes)-1)
        pnode = pnode.destructiveset("repeatnumseparate", nodes[repeatnumindex].repeatnumseparate)
        pnode = pnode.destructiveset("repeatnumcircle", nodes[repeatnumindex].repeatnumcircle)

    # make repeat numbers closer to doner node's
    if random.random() < 0.9:
        donerweight = random.uniform(0, 0.75)
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


# layerlists is the layerlists for the different plants
# layerindex refers to which layer is currently being created in the new plant
# addedsofar is a list of nodes added at this layer so far, to make duplicates less likely
# returns the new node to add to the plant layer and the original node it came from or None if it came from multiple nodes
def random_node_at_layer(layerlists : List[List[List[PlantNode]]], layerindex, addedsofar : List[PlantNode]):
    
    devprint("random node at layer " + str(layerindex))
    # sort by length so that we can access layers that exist
    layerlists = sorted(layerlists, key = len)
    maxlayer = len(layerlists[-1])-1

    
    def random_node_from_layer(chosenlayerindex):
        # choose an i such that all the layers on i and over have enough layers
        i = 0
        while len(layerlists[i])-1 < chosenlayerindex:
            i += 1

        possibleplantlayerlists = layerlists[i:]
        possiblenodes = []
        for plantlayerlist in possibleplantlayerlists:
            for potentialnode in plantlayerlist[chosenlayerindex]:
                if not potentialnode in addedsofar:
                    possiblenodes.append(potentialnode)

        # if all of the nodes have been chosen before pick a new one
        if len(possiblenodes) == 0:
            return random.choice(random.choice(possibleplantlayerlists))
        else:
            return random.choice(possiblenodes)
    
    
    def random_node():
        # most of the time pick from one of the same layer in the else
        random_layer = layerindex

        if layerindex > maxlayer:
            random_layer = random.randint(0, maxlayer)
        elif random.random() < picknodeafterlayerchance(layerindex): # chance for after index
            random_layer = random.randint(layerindex, maxlayer)
        elif random.random() < picknodebeforelayerchance(layerindex):
            random_layer = random.randint(0, max(layerindex-1, 0))
        return random_node_from_layer(random_layer)

    # chance to cross nodes
    if random.random() < crossnodeschance:
        devprint("crossing nodes")
        return crossnodes([random_node(), random_node()]), None
    else:
        original_node = random_node()
        return copy.deepcopy(random_node()), original_node


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


def get_newplant_number_of_layers(plant1_layer_list, plant2_layer_list):
    smallerlength = min(len(plant1_layer_list), len(plant2_layer_list))
    biggerlength = max(len(plant1_layer_list), len(plant2_layer_list))
    
    # pick some number between their layers and also have a chance to add 1
    num_of_layers = random.randint(smallerlength, biggerlength)
    if random.random() < 0.2:
        num_of_layers += 1

    return num_of_layers


def crossplants(plant1, plant2):
    plant1_layer_list : List[List[PlantNode]] = get_plant_layer_list(plant1)
    plant2_layer_list : List[List[PlantNode]] = get_plant_layer_list(plant2)

    newplant_num_of_layers = get_newplant_number_of_layers(plant1_layer_list, plant2_layer_list)
    
    # add layers
    layer_list : List[List[PlantNode]] = [] # the new plant's layer list
    for i in range(newplant_num_of_layers):
        layer_size = random_layer_size([plant1_layer_list, plant2_layer_list], i)
        new_layer = []
        original_nodes = []
        for not_used in range(layer_size):
            newnode, originalnode = random_node_at_layer((plant1_layer_list, plant2_layer_list), i, original_nodes)
            new_layer.append(newnode)
            original_nodes.append(originalnode)
            
        layer_list.append(new_layer)

    
    return Plant(layer_list_to_node(layer_list))
