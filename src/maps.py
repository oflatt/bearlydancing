#!/usr/bin/python

import variables, pygame
variables.draw_loading_text("generating sounds (1/3)")
pygame.display.flip()
from play_sound import play_music, grasslandmusictick, initiategrasslandmusic

variables.draw_loading_text("importing graphics (2/3)")
pygame.display.flip()

import classvar, enemies, graphics, copy, conversations
from Animation import Animation
from graphics import scale_pure
from graphics import GR
from Map import Map
from Rock import Rock
from Exit import Exit
from pygame import Rect
from Conversation import Conversation
from Speak import Speak
from variables import displayscale, fasttestmodep
from EventRequirement import EventRequirement
from random import randint

from mapsvars import *

from honeyhomemaps import *

if not fasttestmodep:
    from forestmaps import *
    from snowmaps import *

# teleportation and stuff#######################################################################
home_map = honeyhome
home_map_name = "honeyhome"
current_map = home_map
current_map_name = 'honeyhome'

nongrasslandmaps = ['honeyhome', 'letter']

# used for making the mapdict
def get_map_coded(name):
    possibles = globals()
    m = possibles.get(name)
    if not m:
        raise NotImplementedError("Map %s not implemented" % name)
    return m

def get_mapdict():
    if fasttestmodep:
        return {"honeyhome": honeyhome,"letter":letter,"outside1":outside1}
    else:
        stringlist = [home_map_name]
        maplist = [home_map]
        index = 0

        while index < len(stringlist):
            for e in maplist[index].exitareas:
                if not e.name in stringlist:
                    stringlist.append(e.name)
                    maplist.append(get_map_coded(e.name))
            index += 1
        newmapdict = {}
        
        for i in range(len(stringlist)):
            newmapdict[stringlist[i]] = maplist[i]
            
        return newmapdict

map_dict = get_mapdict()

def get_map(name):
    return map_dict[name]
    
def set_new_maps(new_mapdict):
    for key in new_mapdict:
        map_dict[key] = new_mapdict[key]

# now that everything is loaded, sort rocks ect
for key in map_dict:
    m = map_dict[key]
    if not m.isscaled:
        m.scale_stuff()

def new_scale_offset():
    global current_map
    variables.scaleoffset = current_map.map_scale_offset
    classvar.player.new_scale_offset()

def change_map_nonteleporting(name):
    global current_map_name
    global current_map
    current_map_name = name
    current_map = get_map(name)
    variables.dirtyrects = [Rect(0,0,variables.width, variables.height)]
    new_scale_offset()

# put player in correct place
classvar.player.teleport(current_map.startpoint[0],
                         current_map.startpoint[1])

def change_map(name, newx, newy):
    oldmapname = current_map_name
    oldplayerx = classvar.player.oldxpos
    oldplayery = classvar.player.oldypos
    
    current_map.lastx = classvar.player.xpos
    current_map.lasty = classvar.player.ypos

    xpos = newx
    ypos = newy

    #now current map is the new one
    change_map_nonteleporting(name)

    halfhoneywidth = int(honeyw/2)*current_map.map_scale_offset
    halfhoneyheight = int(honeyh/2) * current_map.map_scale_offset
    # now handle newx and newy if they are a string
    if newx == "right" or newx == "r":
        xpos = GR[current_map.base]["w"] - halfhoneywidth-1
    elif newx == "left" or newx == "l":
        xpos = -halfhoneywidth+1
    if newy == "up" or newy == "u" or newy == "top" or newy == "t":
        ypos = -halfhoneyheight+1
    elif newy == "down" or newy == "bottom" or newy == "d" or newy == "b":
        ypos = GR[current_map.base]["h"]-halfhoneyheight-1

    #if the new pos is the same
    if newx == "same" or newx == "s":
        xpos = classvar.player.xpos
        if xpos < 0:
            xpos = 0
        if xpos > GR[current_map.base]["w"]- honeyw:
            xpos = GR[current_map.base]["w"]- honeyw

    if newy == "same" or newy == "s":
        ypos = classvar.player.ypos
        if ypos < 0:
            ypos = 0
        if ypos > GR[current_map.base]["h"] - honeyh:
            ypos = GR[current_map.base]["h"] - honeyh
    else:
        ypos *= current_map.map_scale_offset

    #for uselastposq
    if current_map.uselastposq and current_map.lastx != None:
        xpos = current_map.lastx
        ypos = current_map.lasty

    classvar.player.teleport(xpos, ypos)
    if not current_map.playerenabledp:
        classvar.player.change_of_state()
    else:
        classvar.player.soft_change_of_state()

    if classvar.player.collisioncheck(classvar.player.xpos, classvar.player.ypos):
        change_map_nonteleporting(oldmapname)
        classvar.player.soft_change_of_state()
        classvar.player.teleport(oldplayerx, oldplayery)
    else:
        # the map was changed, change the music
        if name == 'honeyhome' and not oldmapname == 'letter':
            play_music('bearhome')
        elif not name in nongrasslandmaps and oldmapname in nongrasslandmaps:
            initiategrasslandmusic()

def teleportplayerhome():
    change_map_nonteleporting(home_map_name)
    classvar.player.teleport(current_map.startpoint[0], current_map.startpoint[1])
    play_music('bearhome')

def initiatemusic():
    if not current_map_name in nongrasslandmaps:
        initiategrasslandmusic()
    
def engage_conversation(cname, floatingconversationp = False):
    if not type(cname) == str:
        raise ValueError("engage_conversation takes a string for the name of the conversation in the current map")

    c = None
    # a floating conversation is one in the floatingconversations dict in conversations module,
    # these are not tied to any map (tutorial conversations)
    if not floatingconversationp:
        c = current_map.getconversation(cname)
    else:
        c = conversations.floatingconversations[cname]

    conversations.currentconversation = c
    
    classvar.player.change_of_state()
    classvar.player.addstoryevent(c.storyevent)

    variables.settings.backgroundstate = variables.settings.state
    if variables.settings.backgroundstate == "battle":
        classvar.battle.pause()
        
        
    variables.settings.state = "conversation"
    
    current = c
    current.updatescreenp = True

    if current.switchtheserocks != None:
        for rockname in current.switchtheserocks:
            current_map.changerock(rockname)

    if len(current.speaks) == 0:
        current.exit_conversation()
        unhiderock(current.unhidethisrock)


def engage_exit(e):
    classvar.player.addstoryevent(e.storyevent)
    change_map(e.name, e.newx, e.newy)

def on_key(key):
    if variables.checkkey("enter", key):
        e = current_map.checkexit()
        c = current_map.checkconversation()
        #if c:
        #    print(c.storyevent)
        #print(classvar.player.storyevents)
        # check for conversations first
        if not c == False:
            engage_conversation(c.name)
        elif not e == False:
            engage_exit(e)
    if variables.checkkey("zoom", key):
        variables.settings.updatezoom(variables.displayscale)
        variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]


def checkexit():
    e = current_map.checkexit()
    if not e == False:
        if e.isbutton == False:
            engage_exit(e)


def checkconversation():
    c = current_map.checkconversation()
    if not c == False:
        if c.isbutton == False:
            engage_conversation(c.name)

def changerock(rockname):
    current_map.changerock(rockname)


def unhiderock(rockname):
    current_map.unhiderock(rockname)

def playerenabledp():
    # just check if they have gotten out of bed at the beginning- from honeyhomemaps
    return not outofbed.activatedp()

# calls the grassland music when appropriate
def musictick():
    if not current_map_name in nongrasslandmaps:
        grasslandmusictick()
