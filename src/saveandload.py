import graphics, variables, pygame, enemies, pickle, classvar, maps, os, conversations
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
    # check to make the dir
    os.makedirs(os.path.dirname(variables.savepath), exist_ok=True)
    
    savelist = [maps.map_dict, conversations.currentconversation,
                classvar.player, classvar.battle, maps.current_map_name]
    with open(variables.savepath, "wb") as f:
        pickle.dump(savelist, f)
    with open(variables.settingspath, "wb") as f:
        pickle.dump(variables.settings, f)
        
# returns a menu
def load():
    m = Menu()
    save0path = variables.savepath
    if (os.path.isfile(os.path.abspath(save0path))):
        if os.path.getsize(os.path.abspath(save0path)) > 0:
            with open(save0path, "rb") as f:
                loadedlist = pickle.load(f)

                mapsdict, conversations.currentconversation, classvar.player, classvar.battle, maps.current_map_name = loadedlist
                if not variables.dontloadmapsdict:
                    loadmaps(mapsdict)

                maps.change_map_nonteleporting(maps.current_map_name)
                # don't start at beginning
                m.firstbootup = False

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()
    
    return m
