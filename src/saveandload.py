import graphics, variables, pygame, enemies, pickle, classvar, maps, os
from classvar import player
from attributes_with_donotload import surfaces_to_donotload_list, assign_attributes, attributes_with_donotload
from Menu import Menu
from variables import displayscale
from Battle import Battle
from enemies import greenie

# can't pickle pygame masks, and problems pickeling pygame surfaces
def save(me):
    player.mask = 0
    mapslist = surfaces_to_donotload_list(maps.get_maplist())
    battleattributes = attributes_with_donotload(classvar.battle)
    savelist = [mapslist,variables.settings, player.xpos/displayscale, player.ypos/displayscale, player.lv, player.exp, player.storyprogress,
                battleattributes, maps.current_map_name]
    with open("bdsave0.txt", "wb") as f:
        pickle.dump(savelist, f)
    player.scale_by_offset()

# newmaps is a list of dict attributes for the map and objects within it
def loadmaps(savedmaps):
    for i in range(len(savedmaps)):
        assign_attributes(maps.map_list[i], savedmaps[i])
        
    
def load():
    m = Menu()
    if (os.path.isfile(os.path.abspath("bdsave0.txt"))):
        if os.path.getsize(os.path.abspath("bdsave0.txt")) > 0:
            f = open("bdsave0.txt", "rb")
            loadedlist = pickle.load(f)
            mapslist, variables.settings, player.xpos, player.ypos, player.lv, player.exp, player.storyprogress, battleattributes, maps.current_map_name = loadedlist

            classvar.battle = Battle(greenie)
            assign_attributes(classvar.battle, battleattributes)
            
            player.xpos *= displayscale
            player.ypos *= displayscale
            loadmaps(mapslist)
            maps.change_map_nonteleporting(maps.current_map_name)
            maps.new_scale_offset()
            # don't start at beginning
            m.firstbootup = False
            print(maps.table.x)

    if (not isinstance(classvar.battle, str)):
        classvar.battle.reset_enemy()

    return m
