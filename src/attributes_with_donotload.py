import pygame
from variables import displayscale, unrounded_displayscale
from Rock import Rock

# this class acts as a dummy value for things values not to be loaded back in, like pygame Surfaces
class DoNotLoad:
    pass

donotload = DoNotLoad()

# unused
def hassurface(listordict):
    checklist = []
    if type(listordict) == dict:
        checklist = list(listordict.values())
    else:
        checklist = listordict
    checkpos = 0
    hassurfacep = False
    while checkpos < len(checklist):
        valtype = type(checklist[checkpos])
        if valtype == pygame.Surface:
            hassurfacep = True
            checkpos = len(checklist)
        elif valtype == dict:
            checklist.extend(checklist[checkpos].values())
            checkpos += 1
        elif valtype in [list, tuple]:
            checklist.extend(checklist[checkpos])
            checkpos += 1
        else:
            checkpos += 1
    return checklist

# a version of hassurface that only checks one layer
def hassurfaceonelayer(listordict):
    checklist = listordict
    if type(listordict) == dict:
        checklist = list(listordict.values())
    hassurfacep = False
    for val in checklist:
        if type(val) == pygame.Surface:
            hassurfacep = True
            break
    return hassurfacep

plaindatalist = (str, bool, float, int, range, type(None))
donotloadtypes = (type(pygame.mask.Mask((10,10))), pygame.Surface)

# the following data items are simply skipped in loading so that loading with different screen sizes works
donotloadkeynames = ["xpos", "x-pos", "x_pos", "x", "lastx", "ypos", "y-pos", "y_pos", "y", "lasty", "collidex", "collidey",
               "w", "width", "height", "h", "screenxoffset", "screenyoffset", "mapdrawx", "mapdrawy", "drawx", "drawy",
                     "newx", "newy", "map_scale_offset", "area", "pos", "startpoint","colliderects", "background_range"]
originalcopykeynames = donotloadkeynames.copy()

# takes an object, and returns a new dict of attributes with any pygame surfaces changed to DoNotLoad
def attributes_with_donotload(objecttoconvert):
    return surfaces_to_donotload_dict(objecttoconvert.__dict__)

# this is basically the same as a call to a pygame rect __dict__ function
def rectdict(pygamerect):
    rectdict = {"x":pygamerect.x,"y":pygamerect.y,"width":pygamerect.width,"height":pygamerect.height}
    return rectdict


# takes a dictionary and returns a new dict with any pygame surfaces changed to None
def surfaces_to_donotload_dict(d):
    newdict = d.copy()
    mapscale = None
    if "map_scale_offset" in d:
        mapscale = d["map_scale_offset"]
    for key in newdict.keys():
        value = newdict[key]
        valuetype = type(value)
        
        if valuetype in donotloadtypes or key in donotloadkeynames:
            newdict[key] = donotload
        elif valuetype in (list, tuple):

            # check if it is the rock list in a map, assumes nothing else uses both word terrain and map_scale_offset
            if key == "terrain" and not mapscale == None:
                newdict[key] = surfaces_to_donotload_terrain(value, mapscale)
            else:
                newdict[key] = surfaces_to_donotload_list(value)
        elif valuetype == dict:
            newdict[key] = surfaces_to_donotload_dict(value)
        elif not valuetype in plaindatalist:
            if valuetype == pygame.Rect:
                    newdict[key] = rectdict(value)
            else:
                # then it must be another object
                newdict[key] = surfaces_to_donotload_dict(value.__dict__)
    return newdict

def surfaces_to_donotload_list(l):
    newlist = l.copy()
    for i in range(len(l)):
        item = newlist[i]
        itemtype = type(item)
        
        if itemtype in donotloadtypes:
            newlist[i] = donotload
        elif itemtype in (list, tuple):
            newlist[i] = surfaces_to_donotload_list(item)
        elif itemtype == dict:
            newlist[i] = surfaces_to_donotload_dict(item)
        elif not itemtype in plaindatalist:
            if itemtype == pygame.Rect:
                newlist[i] = rectdict(item)
            else:
                newlist[i] = surfaces_to_donotload_dict(item.__dict__)
    return newlist

rockroundedscaledkeys = ["x", "y", "w", "h", "collidex", "collidey", "collidew", "collideh"]
rockunroundedscaledkeys = ["background_range"]
def surfaces_to_donotload_terrain(l, mapscale):
    global donotloadkeynames
    # set it so no names get left out
    donotloadkeynames = []
    newlist = l.copy()
    for i in range(len(l)):
        rockdict = attributes_with_donotload(l[i])
        
        for key in rockdict.keys():
            scale = None
            if key in rockroundedscaledkeys:
                scale = mapscale * displayscale
            elif key in rockunroundedscaledkeys:
                scale = mapscale * unrounded_displayscale

            if scale != None:
                if type(rockdict[key]) == dict:
                    for k in rockdict[key].keys():
                        rockdict[key][k] = rockdict[key][k] / scale
                else:
                    rockdict[key] = rockdict[key] / scale
        
        newlist[i] = rockdict
    # set it back so that nothing else is messed up
    donotloadkeynames = originalcopykeynames
    return newlist

# takes an object and re-assigns the attributes to it, skipping donotloads
def assign_attributes(o, attributes):
    if type(o) == pygame.Rect:
        for key in attributes.keys():
            setattr(o, key, attributes[key])
    else:
        assign_attributes_dict(o.__dict__, attributes)
    
def assign_attributes_dict(o, attributes):
    mapscale = None
    if "map_scale_offset" in o:
        mapscale = o["map_scale_offset"]
    for varname in attributes.keys():
        oldval = o[varname]
        val = attributes[varname]
        valtype = type(val)
        
        if valtype == DoNotLoad:
            pass
        elif valtype in plaindatalist:
            o[varname] = val
        elif valtype in [list, tuple]:
            if mapscale != None and varname == "terrain":
                assign_attributes_terrain(o[varname], val, mapscale)
            else:
                assign_attributes_lists(o[varname], val)
        elif valtype == dict:
            # either a normal dict or object attributes, forces checking of type of oldval
            if type(oldval) == dict:
                assign_attributes_dict(oldval, val)
            else:
                #it is another object
                assign_attributes(oldval, val)

def assign_attributes_lists(objectlist, savedlist, scalerectlistp = False):
    if len(savedlist) > len(objectlist):
        # just replace it if the saved list is longer
        # this means that lists that change size need to not have pygame surfaces in them!
        objectlist = savedlist
    else: 
        for i in range(len(savedlist)):
            oldval = objectlist[i]
            val = savedlist[i]
            valtype = type(val)
            
            if valtype == DoNotLoad:
                pass
            elif valtype in plaindatalist:
                objectlist[i] = savedlist[i]
            elif valtype in [list, tuple]:
                assign_attributes_lists(objectlist[i], savedlist[i])
            elif valtype == dict:
                if type(oldval) == dict:
                    assign_attributes_dict(oldval, val)
                else:
                    # must be object
                    if scalerectlistp:
                        pass
                    else:
                        assign_attributes(oldval, val)
        

def assign_attributes_terrain(rocklist, savedrocklist, mapscale):
    print(len(savedrocklist))
    print(len(rocklist))
    for i in range(len(savedrocklist)):
        srock = savedrocklist[i]
        rdict = rocklist[i].__dict__
        for key in srock.keys():
            newval = srock[key]
            scale = None
            if key in rockroundedscaledkeys:
                scale = mapscale * displayscale
            elif key in rockunroundedscaledkeys:
                scale = unrounded_displayscale * mapscale
                
            if scale != None:
                if type(newval) == dict:
                    for k in newval.keys():
                        newval[k] *= scale
                else:
                    newval *= scale
            
            if type(newval) == DoNotLoad:
                pass
            elif type(newval) == dict:
                obj = rdict[key]
                for k in newval.keys():
                    if newval[k] != donotload:
                        setattr(obj, k, newval[k])
            elif type(newval) == list:
                assign_attributes_lists(rdict[key], newval)
            else:
                rdict[key] = newval
