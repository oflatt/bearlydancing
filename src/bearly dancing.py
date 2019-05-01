#!/usr/bin/python
#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame, variables, copy, os, sys, gc, random
from platform import python_implementation
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
from initiatebattle import initiatebattle
import enemies
from enemies import random_enemy
from enemies import devbattletest
import copy


if not variables.testspecs is None:
    if variables.testenemy != None:
        testenemy = copy.copy(enemies.enemyforspecialbattle(variables.testenemy))
    else:
        testenemy = copy.copy(random_enemy("woods"))
    
    testenemy.lv = variables.testspecs['lv']
    testenemy.beatmapspecs = variables.testspecs
    initiatebattle(testenemy)
    menu.firstbootup = False
    variables.settings.menuonq = False


# play main menu music
from play_sound import play_music

play_music("menumusic")
menu.enemyanimation.framerate = (60000/160)*2
menu.enemyanimation.beginning_time = variables.settings.current_time


# key is either a pygame key (an int) or a string for what key was pressed, used for joy stick presses
def onkeydown(key):
    # emergency dev quit
    if variables.devmode and key == variables.devquitkey:
        pygame.quit()
        sys.exit()

    # check if the player is pausing the game
    elif variables.checkkey("escape", key) and not variables.settings.menuonq:
        menu.pause()

    # menu press, also check exiting from the menu, saving from menu
    elif variables.settings.menuonq:
        if variables.checkkey("enter", key) and menu.state == "main":
            if menu.getoption() == "exit":
                global done
                done = True
            elif menu.getoption() == "save":
                save(True)
                variables.saved = True
            else:
                menu.onkey(key)
        else:
            menu.onkey(key)

    # check for dev battle key
    elif variables.devmode and key == variables.devengagebattlekey and variables.settings.state == "world":
        if devbattletest == None:
            initiatebattle(random_enemy())
        else:
            initiatebattle(devbattletest)
            
    # process key in minigame
    elif variables.settings.state == "game" and not variables.settings.menuonq:
        variables.currentgame().keydownfunction(variables.settings.current_time, variables.settings, key)

        
    elif variables.settings.state == "conversation" and conversations.currentconversation != None:
        message = conversations.currentconversation.keyevent(key)
        menu.setmessage(message)
        # check if it was exited to unhide rocks
        if variables.settings.state == "world":
            maps.unhiderock(conversations.currentconversation.unhidethisrock)
    elif variables.settings.state == "world":
        if maps.playerenabledp() and maps.current_map.playerenabledp:
            classvar.player.keypress(key)
        maps.on_key(key)
    elif variables.settings.state == "battle":
        classvar.battle.onkey(key)

def onkeyup(key):
    if variables.settings.menuonq:
        menu.onrelease(key)
    elif variables.settings.state == "world":
        if maps.playerenabledp() and maps.current_map.playerenabledp:
            classvar.player.keyrelease(key)
    elif variables.settings.state == "battle":
        classvar.battle.onrelease(key)
    elif variables.settings.state == "conversation" and conversations.currentconversation != None:
        conversations.currentconversation.keyrelease(key)
    elif variables.settings.state == "game":
        variables.currentgame().keyupfunction(variables.settings.current_time, variables.settings, key)
    
        
def onevent(event):
    global done
    #first check for saving and exiting
    if event.type == pygame.QUIT:
        done = True


    # key down
    if event.type == pygame.KEYDOWN:
        onkeydown(event.key)
    elif event.type == pygame.JOYBUTTONDOWN:
        onkeydown("joy" + str(event.button))


    if event.type == pygame.JOYAXISMOTION:
        keydownpresses = variables.settings.joyaxistokeydown(event)
        if keydown != None:
            onkeydown(keydown)
            
        keyup = variables.settings.joyaxistokeyup(event)
        if keyup != None:
            onkeyup(keyup)

    # key up
    if event.type == pygame.KEYUP:
        onkeyup(event.key)
    elif event.type == pygame.JOYBUTTONUP:
        onkeyup("joy" + str(event.button))


# goes every half second, used for detecting controllers
def onslowtick():
    # detect and register controllers
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        if not joy.get_init():
            joy.init()
            
def ontick():
    # set the saved message if needed
    if (variables.saved):
        menu.saved()
        variables.saved = False

    if variables.settings.slowtickp():
        onslowtick()

    
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
        elif variables.settings.state == "game":
            variables.currentgame().tickfunction(variables.settings.current_time, variables.settings)
    else:
        menu.ontick()

def ondraw():

    
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


    drawnonmenup = True
    if variables.settings.menuonq:
        if menu.mainmenup:
            if menu.state in ["main", "settings"]:
                variables.screen.fill(variables.BLACK)
                drawnonmenup = False
                
    if drawnonmenup:
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
        elif variables.settings.state == "game":
            if variables.settings.menuonq:
                variables.currentgame().drawfunction(menu.pausetime, variables.settings, variables.screen)
            else:
                variables.currentgame().drawfunction(variables.settings.current_time, variables.settings, variables.screen)

    if (variables.settings.menuonq):
        menu.draw()
    # draw message regardless
    if menu != None:
        menu.drawmessage()


    
    if variables.testsmallp:
        # blit red boarder for testing
        variables.screen.fill(variables.RED, Rect(variables.width, 0, 10, variables.height))
        variables.screen.fill(variables.RED, Rect(0, variables.height, variables.width, 10))


    # blit fps
    variables.screen.blit(variables.font.render(str(clock.get_fps()), 0, variables.WHITE), [10, variables.font.get_linesize()])

        
        

    # update the screen
    if len(variables.dirtyrects) > 0 and variables.devmode:
        pygame.draw.rect(variables.screen, variables.BLUE, variables.dirtyrects[0], 1)


    variables.updatescreen()

    # reset dirtyrects
    variables.olddirtyrects = variables.dirtyrects
    variables.dirtyrects = []

    
    

# -------- Main Program Loop -----------
def main():
    while not done:
        # garbage collect if pypy
        if python_implementation() == "PyPy":
            gc.collect_step()
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


main()

# Close the window and quit, this is after the main loop has finished
pygame.quit()

