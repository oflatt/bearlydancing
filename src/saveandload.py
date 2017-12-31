import graphics, variables, pygame, enemies, pickle, classvar, maps, os
from copy import deepcopy
from classvar import player
from Menu import Menu
from Battle import Battle
from enemies import greenie

def loadmaps(maplist):
    for i in range(len(maplist)):
        m = maplist[i]
        m.set_map_scale_offset()
    
    maps.set_new_maps(maplist)

def get_unscaled_maps():
    mlist = maps.map_list
    newlist = []
    for i in range(len(mlist)):
        m = deepcopy(mlist[i])
        m.scale_stuff(1/(m.map_scale_offset*variables.displayscale))
        newlist.append(m)
    return newlist

# can't pickle pygame masks or surfaces
def save(me):
    player.mask = 0
    
    mapslist = get_unscaled_maps()
    savelist = [mapslist,variables.settings, player.xpos/savescalefactor,
                player.ypos/savescalefactor, player.lv, player.exp, player.storyprogress,
                classvar.battle, maps.current_map_name]
    with open("bdsave0.txt", "wb") as f:
        pickle.dump(savelist, f)
    player.scale_by_offset()
        
    
def load():
    m = Menu()
    if (os.path.isfile(os.path.abspath("bdsave0.txt"))):
        if os.path.getsize(os.path.abspath("bdsave0.txt")) > 0:
            f = open("bdsave0.txt", "rb")
            loadedlist = pickle.load(f)
            mapslist, variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress, classvar.battle, maps.current_map_name = loadedlist
            player.xpos *= savescalefactor
            player.ypos *= savescalefactor
            loadmaps(mapslist)
            maps.change_map_nonteleporting(maps.current_map_name)
            # don't start at beginning
            m.firstbootup = False

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()

    return m
