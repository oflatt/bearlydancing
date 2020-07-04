import math, random
from pygame import gfxdraw
from pygame import Surface, SRCALPHA, Rect

from rdraw.pointlist import rotatepointlist, offsetpointlist, getlistbounds, listangleatindex
from rdraw.rdrawsoil import dirtcolor
from rdraw.addtexture import addtexture
from variables import brighten, devprint

from .constants import potwidth


def addtoshiftlist(shiftlist, newmaxx, shiftchance):
    
    numbertoadd = newmaxx-len(shiftlist)+2
    if len(shiftlist) == 0:
        currentshiftamount = 0
    else:
        currentshiftamount = shiftlist[-1]
    for i in range(int(numbertoadd)):
        if random.random() < shiftchance + shiftchance*(i+newmaxx)/newmaxx:
            if random.random() < 0.5:
                currentshiftamount += 1
            else:
                currentshiftamount -= 1
                
        shiftlist.append(currentshiftamount)

# offsetlist is a shared list of the shift amounds for each x position in the list
def shiftpointlist(pointlistin, shiftlist, shiftchance, widthscalar, heightscalar):
    l = pointlistin.copy()

    maxx = pointlistin[int(len(pointlistin)/2)][0]
    if len(shiftlist) <= maxx:
        addtoshiftlist(shiftlist, maxx, shiftchance)

    for i in range(int(len(l)/2)):
        newx = l[i][0]*heightscalar
        # use the x pos as the index into shiftlist
        currentshift = shiftlist[int(l[i][0])]
        l[i] = (newx, l[i][1]*widthscalar+ currentshift)
        l[-i-1] = (newx, l[-i-1][1]*widthscalar+currentshift)

    return l


# shifts point lists together and returns a list of polygon lists
def shiftpointlists(plantshapelist, shiftchance, widthscalar, heightscalar):
    listofpolygons = []
    shiftlist = []

    # approximate how many shifts are needed with length of list
    addtoshiftlist(shiftlist, len(plantshapelist[0].polygonlist)/2, shiftchance)

    for plantshape in plantshapelist:
        listofpolygons.append(shiftpointlist(plantshape.polygonlist, shiftlist, shiftchance, widthscalar, heightscalar))

    for plist in listofpolygons:
        if len(plist) % 2 != 0:
            raise Exception("polygonlist must be an even length, something went wrong")
    return listofpolygons



# returns a list of transformed polygon lists from the shapelist
def transformtopointlists(plantshapelist, shiftchance, angle, widthscalar, heightscalar):
    
    listofpolygonlists = shiftpointlists(plantshapelist, shiftchance, widthscalar, heightscalar)
    
    
    for i in range(len(listofpolygonlists)):
        listofpolygonlists[i] = rotatepointlist(listofpolygonlists[i], angle, offsetresult=(0,0))
    
    return listofpolygonlists


# returns a list of index positions in a polygon list on which to spawn new nodes
# takes the number of nodes to put on, the length of the parent node polygon list
# and the percent of the polygon list that is available for spawning on
def getfuturenodeindexpositions(numberofnodes, polygonlistlength, percentofbranch, branchoffset):

    percentofbranch = min(percentofbranch, (1-branchoffset))
    
    # first make dispersed distruibution for the new nodes
    dispersedpositions = []
    total = 0
    for x in range(numberofnodes+1):
        # half of the spacing is random
        dispersedpositions.append((random.random()/numberofnodes)/2 + (1/numberofnodes)/2)
        total += dispersedpositions[-1]

    # normalize it to fit into 1
    normalize_factor = 1.0/total
    normalize_factor = normalize_factor * polygonlistlength * percentofbranch

    # offset
    offset = (polygonlistlength/2) - (polygonlistlength/2)*percentofbranch - (polygonlistlength/2) * branchoffset
    
    # omit the last space because it is now not needed
    dispersedpositions.pop()

    indexes = []
    currentpos = offset
    insecondhalf = False
    
    # now translate it into the space of the part of the polygonlist
    for i in range(len(dispersedpositions)):
        currentpos += dispersedpositions[i] * normalize_factor
        if not insecondhalf:
            if currentpos > (polygonlistlength/2) - (polygonlistlength/2)*branchoffset:
                currentpos = currentpos + (polygonlistlength/2)*branchoffset * 2
                insecondhalf = True
        
        indexes.append(int(currentpos))

    # should be the same length as number of nodes
    if not numberofnodes == len(indexes):
        raise Exception("Bad number of indexes")
    for i in indexes:
        if i < 0:
            raise Exception("Future index position negative")
        elif i > polygonlistlength:
            raise Exception ("Future index position to large")
    return indexes


# returns a new or the old surface with the input node added
# also returns the polygon list for the first node that has been translated, along with the offset for that polygon list
# finally, it returns an offset needed because of any resizing of the surface
def surface_with_node(surface, node, angle, offset_in, current_resize_offset, widthscalar, heightscalar):
    transformedlists = transformtopointlists(node.plantshapelist,
                                        node.shiftchance, angle,
                                        widthscalar, heightscalar)

    mainloffset = None
    mainltranslated = None

    def currentoffset():
        return (offset_in[0] + current_resize_offset[0], offset_in[1] + current_resize_offset[1])

    def surface_offset(pointlist_bounds):
        return Rect(currentoffset()[0]-node.anchor[0]+pointlist_bounds[0], currentoffset()[1]-node.anchor[1]+pointlist_bounds[1], pointlist_bounds.width, pointlist_bounds.height)

    # go through all the plantshapes and their corresponding transformed lists
    for i in range(len(transformedlists)):
        currentlist = transformedlists[i]
        bounds = getlistbounds(currentlist)

        # make the surface
        shape_surface = Surface((bounds.width, bounds.height), SRCALPHA)
        # translate points into this surface
        shiftedlist = offsetpointlist(currentlist, (-bounds[0], -bounds[1]))

        # draw the plant shape onto the new surface
        plantshape = node.plantshapelist[i]
        if plantshape.fillcolor != None:
        
            gfxdraw.filled_polygon(shape_surface, shiftedlist, plantshape.fillcolor)
        if plantshape.outlinecolor != None:
            gfxdraw.polygon(shape_surface, shiftedlist, plantshape.outlinecolor)


        # apply the texture if any
        for ptexture in plantshape.textures:
            addtexture(shape_surface, ptexture)

            
        # now check if resizing is needed
        newsurfacerect = surface.get_rect().union(surface_offset(bounds))
        
        if not newsurfacerect == surface.get_rect():
            
            new_surface = Surface((newsurfacerect.width, newsurfacerect.height), SRCALPHA)
            new_surface.blit(surface, (-newsurfacerect.x, -newsurfacerect.y))

            current_resize_offset = (current_resize_offset[0]-newsurfacerect.x, current_resize_offset[1]-newsurfacerect.y)

            surface = new_surface
            
            devprint("Resized surface to " + str(new_surface.get_width()) + " by " + str(new_surface.get_height()))

        surface.blit(shape_surface, surface_offset(bounds))

        # also save the first list for other nodes to go off of
        if i == 0:
            # save the offset of l without the resizing
            mainloffset = surface_offset(bounds)
            # also remove the current resize offset
            mainloffset = (mainloffset[0] - current_resize_offset[0], mainloffset[1]-current_resize_offset[1])
            mainltranslated = shiftedlist
            
            
    return surface, mainltranslated, mainloffset, current_resize_offset


def drawplant(head_node):
    devprint("drawing plant")
    
    surface = Surface((40, 43), SRCALPHA)
    rootpos = (surface.get_width()/2, surface.get_height()-3)
    
    
    # the stack has the node, the currentx, and the currenty for each node in it
    # currentx and currenty are without resizing of the surface
    stack = []
    # keeps track of offset needed because of resizing the surface
    resizeoffset = (0, 0)

    for i in range(head_node.repeatnumseparate):
        stack.append(head_node)
        firstx = potwidth * random.random() * head_node.brancharea + rootpos[0]
        stack.append(firstx)
        stack.append(rootpos[1])
        stack.append(math.pi/2) # base angle strait up to start with
    
    callcount = 0

    while len(stack) != 0 and callcount < 1000:
        
        callcount += 1
        base_angle = stack.pop()
        currenty = stack.pop()
        currentx = stack.pop()
        node = stack.pop()
        
        randomspacings = [0]
        spacingLength = 0
        for i in range(node.repeatnumcircle-1):
            randomspacings.append(random.uniform(node.anglespace-node.anglevariance*node.anglespace, node.anglespace+node.anglevariance*node.anglespace))
            spacingLength += randomspacings[i+1]

        startspacing = random.uniform(-node.anglevariance*node.anglespace, node.anglevariance*node.anglespace)/2 * random.choice((-1, 1))
        
        # start angle so that it points up on average
        angle = base_angle + startspacing - (spacingLength/2)  + node.angleoffset*random.choice((-1, 1))

        # update the random spacing to be final angles
        for i in range(len(randomspacings)):
            angle = angle + randomspacings[i]
            randomspacings[i] = angle

        for i in range(node.repeatnumcircle):
            # draw all the plantshapes at this angle
            # pick a random angle out of the list
            angle = randomspacings.pop(random.randint(0, len(randomspacings)-1))

            widthscalar = 1 + random.random()*node.widthvariance
            heightscalar = 1 + random.random()*node.heightvariance

            # now add the current node
            surface, mainltranslated, mainloffset, new_resize_offset = surface_with_node(surface, node, angle, (currentx, currenty), resizeoffset,  widthscalar, heightscalar)
            resizeoffset = new_resize_offset

            
            # find the new currentx and currenty
            mainlistlen = len(mainltranslated)

            
            # add all the children at the current position
            for childnode in node.children:
                futureindexpositions = getfuturenodeindexpositions(childnode.repeatnumseparate, mainlistlen, childnode.brancharea, childnode.branchoffset)
                for i in range(childnode.repeatnumseparate):
                    futurex = mainltranslated[futureindexpositions[i]][0]+mainloffset[0]
                    futurey = mainltranslated[futureindexpositions[i]][1]+mainloffset[1]
                    stack.append(childnode)
                    stack.append(futurex)
                    stack.append(futurey)
                    futureangle = listangleatindex(mainltranslated, futureindexpositions[i])
                    stack.append(futureangle)

    finalsurfaceanchor = (rootpos[0] + resizeoffset[0], rootpos[1]+resizeoffset[1])
                
    # draw dirt clumps at bottom
    clumpradius = 4
    clumprange = 14
    clumpnum = 4
    
    for i in range(clumpnum):
        gfxdraw.filled_circle(surface, int(finalsurfaceanchor[0] + i * clumprange/clumpnum - clumprange/2)+1,
                       int(finalsurfaceanchor[1]),
                       int(random.uniform(clumpradius/3, clumpradius)),
                        brighten(dirtcolor, -10))
        
    return surface, finalsurfaceanchor 
