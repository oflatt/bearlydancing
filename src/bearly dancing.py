#!/usr/bin/python
import pygame, variables, copy, os, sys
from pygame import Rect


variables.load_properties()
variables.draw_loading_tips()

# determine if everything should be re-loaded
if not os.path.isfile(os.path.abspath(variables.settingspath)) and not variables.newworldnever:
    variables.newworldeachloadq = True

# now go ahead and load everything in
import maps
import conversations, classvar
from saveandload import save, load

# save the properties to record how many things needed to be loaded
variables.save_properties()

pygame.display.set_caption("Bearly Dancing")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

menu = load()

maps.new_scale_offset()

# for skipsteve add the event
if variables.skipsteve:
    classvar.player.addstoryevent("beatsteve")

#clear all the events so it does not mess up the game when it loads
pygame.event.get()

# Loop variable
done = False

# if the testspecs are set, use it and initiate a battle
from initiatestate import initiatebattle
from enemies import random_enemy
from enemies import devbattletest
import copy
if variables.testspecs != None:
    testenemy = copy.copy(random_enemy("woods"))
    testenemy.lv = variables.testspecs['lv']
    testenemy.beatmaprules = variables.testspecs['rules']
    initiatebattle(testenemy)
    menu.firstbootup = False
    variables.settings.menuonq = False

# play main menu music
from play_sound import play_music

play_music("menumusic")
menu.enemyanimation.framerate = (60000/160)*2
menu.enemyanimation.beginning_time = variables.settings.current_time


def onevent(event):
    global done
    #first check for saving and exiting
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN and event.key == variables.devquitkey:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN and variables.checkkey("enter", event.key) and variables.settings.menuonq:
        if menu.state == "main":
            if menu.getoption() == "exit":
                done = True
            elif menu.getoption() == "save":
                save(True)
                variables.saved = True

    # process key in minigame
    if variables.settings.state == "game":
        variables.currentgame().inputfunction(variables.settings.current_time, variables.settings, event)

        
    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
        # check for dev battle key
        if variables.devmode and event.key == variables.devengagebattlekey and variables.settings.state == "world":
            if devbattletest == None:
                initiatebattle(random_enemy())
            else:
                initiatebattle(devbattletest)

        elif (not variables.settings.menuonq):
            if variables.settings.state == "conversation" and conversations.currentconversation != None:
                message = conversations.currentconversation.keyevent(event.key)
                menu.setmessage(message)
                # check if it was exited to unhide rocks
                if variables.settings.state == "world":
                    maps.unhiderock(conversations.currentconversation.unhidethisrock)
            elif variables.settings.state == "world":
                if maps.playerenabledp() and maps.current_map.playerenabledp:
                    classvar.player.keypress(event.key)
                maps.on_key(event.key)
            elif variables.settings.state == "battle":
                classvar.battle.onkey(event.key)

            # also check if the player is pausing the game
            if variables.checkkey("escape", event.key):
                if not variables.settings.menuonq:
                    menu.pause()
        else:
            menu.onkey(event.key)


    # User let up on a key
    elif event.type == pygame.KEYUP:
        if (not variables.settings.menuonq):
            if variables.settings.state == "world":
                if maps.playerenabledp() and maps.current_map.playerenabledp:
                    classvar.player.keyrelease(event.key)
            elif variables.settings.state == "battle":
                classvar.battle.onrelease(event.key)
            elif variables.settings.state == "conversation" and conversations.currentconversation != None:
                conversations.currentconversation.keyrelease(event.key)
        else:
            menu.onrelease(event.key)


def ontick():
    if variables.settings.state == "game":
        variables.currentgame().tickfunction(variables.settings.current_time, variables.settings)
    
    if variables.settings.state == "world" or (variables.settings.state == "conversation" and variables.settings.backgroundstate == "world"):
        maps.musictick()
    if (not variables.settings.menuonq):
        if variables.settings.state == "world":
            classvar.player.move()
            maps.checkconversation()
            maps.checkexit()
            maps.current_map.on_tick()
        elif variables.settings.state == "battle":
            classvar.battle.ontick()
    else:
        menu.ontick()

def ondraw():
    # draw saved
    if (variables.saved):
        menu.saved()
        variables.saved = False

    def draw_world():
        #fill edges in with black
        screenxoffset = maps.current_map.screenxoffset()
        if screenxoffset != 0:
            variables.screen.fill(variables.BLACK,
                                  Rect(0, 0, screenxoffset+1, variables.height))
            variables.screen.fill(variables.BLACK,
                                  Rect(variables.width-screenxoffset-2, 0, screenxoffset+3, variables.height))
            
        classvar.player.update_drawpos()
        
        maps.current_map.draw([classvar.player.mapdrawx, classvar.player.mapdrawy])
        if maps.playerenabledp() and maps.current_map.playerenabledp:
            classvar.player.draw()
        maps.current_map.draw_foreground([classvar.player.mapdrawx, classvar.player.mapdrawy])


    drawworldp = True
    if variables.settings.menuonq:
        if menu.mainmenup:
            if menu.state in ["main", "settings"]:
                variables.screen.fill(variables.BLACK)
                drawworldp = False
    if drawworldp:
        if variables.settings.state == "conversation":
            if variables.settings.backgroundstate == "world":
                draw_world()
            else:
                variables.screen.fill(variables.BLACK)
                classvar.battle.draw()
            conversations.currentconversation.draw()
        elif variables.settings.state == "world":
            draw_world()
        elif variables.settings.state == "battle":
            variables.screen.fill(variables.BLACK)
            classvar.battle.draw()

    if (variables.settings.menuonq):
        menu.draw()
    # draw message regardless
    if menu != None:
        menu.drawmessage()


    # blit fps
    variables.screen.blit(variables.font.render(str(clock.get_fps()), 0, variables.WHITE), [10, variables.font.get_linesize()])

    if variables.testsmallp:
        # blit red boarder for testing
        variables.screen.fill(variables.RED, Rect(variables.width, 0, 10, variables.height))
        variables.screen.fill(variables.RED, Rect(0, variables.height, variables.width, 10))


    if variables.settings.state == "game":
        variables.currentgame().drawfunction(variables.settings.current_time, variables.settings, variables.screen)
        
    # Go ahead and update the screen with what we've drawn.
    if variables.settings.state != "game":
        if len(variables.dirtyrects) > 0 and variables.devmode:
            pygame.draw.rect(variables.screen, variables.BLUE, variables.dirtyrects[0], 1)


        variables.updatescreen()

        # reset dirtyrects
        variables.olddirtyrects = variables.dirtyrects
        variables.dirtyrects = []

    
    

# -------- Main Program Loop -----------
while not done:
    # add the past tick to the current time
    if not variables.generatingbeatmapp:
        variables.settings.current_time += clock.get_time()
    else:
        # set it to false, done generating
        variables.generatingbeatmapp = False
        # do not add the time to the clock
        clock.get_time()


    # --- Event Processing-
    for event in pygame.event.get():
        onevent(event)
    
        
    # --- Game Logic
    ontick()    
    
    # --- Drawing Code
    ondraw()
    
    # We want as many frames as possible to reduce likelyhood for mismatch with screen refresh and tearing
    clock.tick_busy_loop(0)


# Close the window and quit, this is after the main loop has finished
pygame.quit()

