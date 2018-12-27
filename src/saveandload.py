import graphics, variables, pygame, enemies, classvar, maps, os, conversations
from copy import deepcopy
from Menu import Menu
from Battle import Battle
import dill as pickle
from stathandeling import explv, lvexp
from play_sound import soundpackkeys, scales

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

    conversationname = None
    if conversations.currentconversation != None:
        converstaionname = conversations.currentconversation.name
    
    savelist = [maps.map_dict, conversationname,
                classvar.player, classvar.battle, maps.current_map_name, conversations.floatingconversations]
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
                tempplayer = None
                mapsdict, tempcname, tempplayer, classvar.battle, maps.current_map_name, floatingtemp = loadedlist
                if not variables.dontloadplayer:
                    classvar.player = tempplayer
                else:
                    classvar.player.xpos = tempplayer.xpos
                    classvar.player.ypos = tempplayer.ypos
                    for x in range(50):
                        classvar.player.addstoryevent("bed")
                        
                if variables.lvcheat != 0:
                    classvar.player.exp = lvexp(explv(classvar.player.exp)+variables.lvcheat)
                if variables.addallrewards:
                    for k in soundpackkeys:
                        classvar.player.addreward(k)
                    for k in scales.keys():
                        classvar.player.addreward(k)
                    
                if not variables.dontloadmapsdict:
                    conversations.floatingconversations = floatingtemp
                    loadmaps(mapsdict)
                    if tempcname in conversations.floatingconversations.keys():
                        conversations.currentconversation = conversations.floatingconversations[tempckey]
                    else:
                        conversations.currentconversation = maps.map_dict[maps.current_map_name].getconversation(tempcname)

                maps.change_map_nonteleporting(maps.current_map_name)
                # don't start at beginning
                m.firstbootup = False
                
    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()
    
    return m
