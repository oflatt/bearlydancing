import pygame

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

# takes an object, and returns a new dict of attributes with any pygame surfaces changed to DoNotLoad
def attributes_with_donotload(objecttoconvert):
    return surfaces_to_donotload_dict(objecttoconvert.__dict__)

# this is basically the same as a call to a pygame rect __dict__ function
def rectdict(pygamerect):
    return {"x":pygamerect.x,"y":pygamerect.y,"width":pygamerect.width,"height":pygamerect.height}

plaindatalist = (str, bool, float, int, range, type(None))
donotloadtypes = (type(pygame.mask.Mask((10,10))), pygame.Surface)

# takes a dictionary and returns a new dict with any pygame surfaces changed to None
def surfaces_to_donotload_dict(d):
    newdict = d.copy()
    for key in newdict.keys():
        value = newdict[key]
        valuetype = type(value)
        if valuetype in donotloadtypes:
            newdict[key] = donotload
        elif valuetype in (list, tuple):
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
