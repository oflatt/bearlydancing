import argparse, pygame

testsmallp = False
devmode = True
# skip the fight with steve, add the event to the player
skipsteve = True
# adds all the soundpacks and keys to the player
addallrewards = False
# generates a new world on load no matter what
newworldeachloadq = False
# allows specific graphics functions to override and make new generated graphics
allownewworldoverridep = True
# this overrides the generation of a new set of graphics for a new game
newworldnever = False
# this is for not loading the maps from the save file, to test new map changes
dontloadmapsdict = False
# this is to get a fresh player with no player attributes
dontloadplayer = False
# get a fresh settings file
dontloadsettings = False
# only loads first couple of maps
fasttestmodep = False
# adds to player level when loading
lvcheat = 0

# if None it does nothing, if it is a dictionary for "specs" it goes directly into a battle with those specs
testspecs = None#{'maxtime' : 20, 'lv' : 4, 'rules' : ["alternating"]}

devlosebattlekey = pygame.K_BACKSLASH
devwinbattlekey = pygame.K_END
devengagebattlekey = pygame.K_END
devquitkey = pygame.K_RCTRL

# this is the mode for the finished product- it just turns off all other development modes
exportmode = False

parser = argparse.ArgumentParser()

parser.add_argument('--exportmode', "- run bearly dancing in the mode intended for release.", action = 'store_true')

parser.add_argument('--generatenorestart', "- generate all graphics but do not reset save files.",action = 'store_true')

parser.add_argument('--restartnogeneration', "- restart save files but don't generate new graphics.",action = 'store_true')

parser.add_argument('--novideomode', "- don't initialize the display or draw anything.",action = 'store_true')

parser.add_argument('--fasttestmode', "- only load the first couple of maps.", action = 'store_true')

args = parser.parse_args()

if args.exportmode:
    exportmode = True

if args.restartnogeneration:
    newworldeachloadq = False
    newworldnever = True
    dontloadmapsdict = True
    dontloadplayer = True
    dontloadsettings = True

if args.generatenorestart:
    newworldeachloadq = True
    newworldnever = False
    dontloadmapsdict = False
    dontloadplayer = False
    dontloadsettings = False

if args.fasttestmode:
    fasttestmodep = True
    
if exportmode:
    testsmallp = False
    devmode = False
    skipsteve = False
    addallrewards = False
    newworldnever = False
    newworldeachloadq = False
    allownewworldoverridep = False
    dontloadmapsdict = False
    dontloadplayer = False
    dontloadsettings = True
    fasttestmodep = False
    lvcheat = 0
    testspecs = None

    
# only print if devmode is on
def devprint(s):
    if devmode:
        print(s)
