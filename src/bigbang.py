#!/usr/bin/python
import pygame, variables, copy, os
from pygame import Rect

variables.load_properties()
variables.draw_loading_text("importing graphics (1/2)")
pygame.display.flip()

# determine if everything should be re-loaded
if not os.path.isfile(os.path.abspath("bdsave0.txt")):
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

#clear all the events so it does not mess up the game when it loads
pygame.event.get()

# Loop variable
done = False


# -------- Main Program Loop -----------
while not done:
    
    # add the past tick to the current time
    variables.settings.current_time += clock.get_time()
    
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        #first check for saving and exiting
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key in variables.settings.enterkeys and variables.settings.menuonq:
            if menu.state == "main":
                if menu.getoption() == "exit":
                    done = True
                elif menu.getoption() == "save":
                    save(menu)
                    menu.saved()

        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            if event.key in variables.settings.escapekeys:
                #if we are turning on the menu pause the beatmaps
                if not variables.settings.menuonq:
                    menu.pause()
                else:
                    menu.resume()
                
            if (not variables.settings.menuonq):
                if variables.settings.state == "conversation":
                    conversations.currentconversation.keypress(event.key)
                elif variables.settings.state == "world":
                    if maps.playerenabledp() and maps.current_map.playerenabledp:
                        classvar.player.keypress(event.key)
                    maps.on_key(event.key)
                elif variables.settings.state == "battle":
                    classvar.battle.onkey(event.key)
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
                elif variables.settings.state == "conversation":
                    conversations.currentconversation.keyrelease(event.key)
            else:
                menu.onrelease(event.key)
    
    # --- Game Logic
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

    # --- Drawing Code
    def draw_world():
        classvar.player.update_drawpos()
        
        maps.current_map.draw([classvar.player.mapdrawx, classvar.player.mapdrawy])
        if maps.playerenabledp() and maps.current_map.playerenabledp:
            classvar.player.draw()
        maps.current_map.draw_foreground([classvar.player.mapdrawx, classvar.player.mapdrawy])

        #fill edges in with black
        screenxoffset = maps.current_map.screenxoffset
        if screenxoffset != 0:
            variables.screen.fill(variables.BLACK,
                                  Rect(0, 0, screenxoffset, variables.height))
            variables.screen.fill(variables.BLACK,
                                  Rect(variables.width-screenxoffset-1, 0, screenxoffset+1, variables.height))

    drawworldp = True
    if variables.settings.menuonq:
        if menu.mainmenup:
            if menu.state == "main":
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
            # first fill in old rects
            for dr in variables.dirtyrects:
                variables.screen.fill(variables.BLACK, dr)
            # update these parts
            pygame.display.update(variables.dirtyrects)
            variables.dirtyrects = []
            
            classvar.battle.draw()

            

    if (variables.settings.menuonq):
        menu.draw()


    # blit fps
    fpspic = variables.font.render(str(int(clock.get_fps())))
    if variables.settings.state == "battle":
        frect = pygame.Rect(20,20,fpspic.get_width()*2,fpspic.get_height())
        variables.screen.fill(variables.BLACK, fpsrect)
        variables.dirtyrects.append(frect)
    variables.screen.blit(fpspic, 0, variables.WHITE), [20, 20])
        

    if variables.testsmallp:
        # blit red boarder for testing
        variables.screen.fill(variables.RED, Rect(variables.width, 0, 10, variables.height))
        variables.screen.fill(variables.RED, Rect(0, variables.height, variables.width, 10))
    
    # Go ahead and update the screen with what we've drawn.
    if variables.settings.state != "battle":
        pygame.display.flip()
    else:
        # just update dirtyrects
        pygame.display.update(variables.dirtyrects)
            

    # Limit frames per second
    clock.tick(60)

# Close the window and quit, this is after the main loop has finished
pygame.quit()
