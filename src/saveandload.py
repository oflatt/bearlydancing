import graphics, variables, pygame, enemies, classvar, maps, os, conversations
from copy import deepcopy
from Menu import Menu
from Battle import Battle
import dill as pickle
from stathandeling import explv, lvexp

def loadmaps(mapdict):
    maps.set_new_maps(mapdict)


# can't pickle pygame masks or surfaces
def save(manualp):
    # check to make the dir
    try:
        os.makedirs(variables.savefolderpath, exist_ok=True)
    except FileExistsError:
        pass

    try:
        os.makedirs(variables.manualsavebackuppath, exist_ok=True)
    except FileExistsError:
        pass
    
    savelist = [maps.map_dict, conversations.currentconversation,
                classvar.player, classvar.battle, maps.current_map_name]
    with open(variables.savepath, "wb") as f:
        pickle.dump(savelist, f)
    with open(variables.settingspath, "wb") as f:
        pickle.dump(variables.settings, f)

    if(manualp):
        with open(os.path.join(variables.manualsavebackuppath, "bdsave.txt"), "wb") as f:
            pickle.dump(savelist, f)
        with open(os.path.join(variables.manualsavebackuppath, "bdsettings.txt"), "wb") as f:
            pickle.dump(variables.settings, f)


    
        
# returns a menu
def load():
    m = Menu()
    save0path = variables.savepath
    if (os.path.isfile(save0path)):
        if os.path.getsize(save0path) > 0:
            with open(save0path, "rb") as f:
                loadedlist = pickle.load(f)

                mapsdict, conversations.currentconversation, classvar.player, classvar.battle, maps.current_map_name = loadedlist
                if variables.lvcheat != 0:
                    classvar.player.exp = lvexp(explv(classvar.player.exp)+variables.lvcheat)
                if not variables.dontloadmapsdict:
                    loadmaps(mapsdict)

                maps.change_map_nonteleporting(maps.current_map_name)
                # don't start at beginning
                m.firstbootup = False
                
    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()
    
    return m
