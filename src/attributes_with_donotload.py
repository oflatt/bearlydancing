import pygame
from variables import displayscale

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
poskeynames = ["xpos", "x-pos", "x_pos", "x", "lastx", "ypos", "y-pos", "y_pos", "y", "lasty", "collidex", "collidey",
               "w", "width", "height", "h"]
scalerectnames = ["background_range"]
scalelistnames = ["area", "pos"]

# takes an object, and returns a new dict of attributes with any pygame surfaces changed to DoNotLoad
def attributes_with_donotload(objecttoconvert):
    return surfaces_to_donotload_dict(objecttoconvert.__dict__)

# this is basically the same as a call to a pygame rect __dict__ function
def rectdict(pygamerect, keyname = None):
    rectdict = {"x":pygamerect.x,"y":pygamerect.y,"width":pygamerect.width,"height":pygamerect.height}
    if keyname in scalerectnames:
        for key in rectdict.keys():
            rectdict[key] /= displayscale
    return rectdict


# takes a dictionary and returns a new dict with any pygame surfaces changed to None
def surfaces_to_donotload_dict(d):
    newdict = d.copy()
    for key in newdict.keys():
        value = newdict[key]
        valuetype = type(value)

        # unscale for saving
        if key in poskeynames:
            if valuetype in [int, float]:
                newdict[key] = value / displayscale
        
        if valuetype in donotloadtypes:
            newdict[key] = donotload
        elif valuetype in (list, tuple):
            # unscale for saving
            if key in scalelistnames:
                for i in range(len(value)):
                    newdict[key][i] = value[i] / displayscale
            else:
                newdict[key] = surfaces_to_donotload_list(value)
        elif valuetype == dict:
            newdict[key] = surfaces_to_donotload_dict(value)
        elif not valuetype in plaindatalist:
            if valuetype == pygame.Rect:
                newdict[key] = rectdict(value, key)
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

# takes an object and re-assigns the attributes to it, skipping donotloads
def assign_attributes(o, attributes, varname = None):
    if type(o) == pygame.Rect:
        scalefactor = 1
        if varname in scalerectnames:
            scalefactor = displayscale
        for key in attributes.keys():
            setattr(o, key, attributes[key]*scalefactor)
    else:
        assign_attributes_dict(o.__dict__, attributes)
    
def assign_attributes_dict(o, attributes):
    for varname in attributes.keys():
        oldval = o[varname]
        val = attributes[varname]
        valtype = type(val)
        # scale back up for saving
        if varname in poskeynames:
            if valtype in [int, float]:
                val *= displayscale
        
        if valtype == DoNotLoad:
            pass
        elif valtype in plaindatalist:
            o[varname] = val
        elif valtype in [list, tuple]:
            if varname in scalelistnames:
                for i in range(len(val)):
                    val[i] *= displayscale
            assign_attributes_lists(o[varname], val)
        elif valtype == dict:
            # either a normal dict or object attributes, forces checking of type of oldval
            if type(oldval) == dict:
                assign_attributes_dict(oldval, val)
            else:
                #it is another object
                assign_attributes(oldval, val, varname)

def assign_attributes_lists(objectlist, savedlist):
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
                    assign_attributes(oldval, val)
        
                
        
