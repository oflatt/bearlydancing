import graphics, variables, pygame, enemies, pickle, classvar, maps, os
from copy import deepcopy
from Menu import Menu
from Battle import Battle
from enemies import greenie

def loadmaps(mapdict):
    for key in mapdict:
        m = mapdict[key]
        m.set_map_scale_offset()
    
    maps.set_new_maps(mapdict)


# can't pickle pygame masks or surfaces
def save(me):
    
    savelist = [maps.map_dict,variables.settings, classvar.player,
                classvar.battle, maps.current_map_name]
    with open("bdsave0.txt", "wb") as f:
        pickle.dump(savelist, f)
        
# returns a menu
def load():
    m = Menu()
    if (os.path.isfile(os.path.abspath("bdsave0.txt"))):
        if os.path.getsize(os.path.abspath("bdsave0.txt")) > 0:
            f = open("bdsave0.txt", "rb")
            loadedlist = pickle.load(f)
            mapsdict, variables.settings, classvar.player, classvar.battle, maps.current_map_name = loadedlist
            loadmaps(mapsdict)
            maps.change_map_nonteleporting(maps.current_map_name)
            # don't start at beginning
            m.firstbootup = False

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()
    
    return m
