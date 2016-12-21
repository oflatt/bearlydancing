#!/usr/bin/python
import pygame, variables
from variables import settings

LOADINGTEXT = pygame.transform.scale2x(variables.font.render("LOADING...", 0, variables.WHITE))
variables.wide_screen.blit(LOADINGTEXT, [0, 0])
pygame.display.flip()

import maps
import conversations, classvar, Menu

Menu.load()

pygame.display.set_caption("Bearly Dancing")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

maps.new_scale_offset()

menu = Menu.Menu()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key in settings.enterkeys and settings.menuonq and \
                        menu.options[menu.option] == "exit":
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settings.menuonq = not settings.menuonq
                classvar.player.change_of_state()
            if (not settings.menuonq):
                if settings.state == "conversation":
                    conversations.currentconversation.keypress(event.key)
                elif settings.state == "world":
                    classvar.player.keypress(event.key)
                    maps.on_key(event.key)
                elif settings.state == "battle":
                    classvar.battle.onkey(event.key)
            else:
                menu.onkey(event.key)


        # User let up on a key
        elif event.type == pygame.KEYUP:
            if (not settings.menuonq):
                if settings.state == "world":
                    classvar.player.keyrelease(event.key)
                elif settings.state == "battle":
                    classvar.battle.onrelease(event.key)

    # --- Game Logic
    if (not settings.menuonq):
        if settings.state == "world":
            classvar.player.move()
            maps.checkexit()
            maps.current_map.on_tick()
            maps.checkconversation()
        elif settings.state == "battle":
            classvar.battle.ontick()

    # --- Drawing Code
    variables.screen.fill(variables.WHITE)
    if settings.state == "conversation":
        maps.current_map.draw(classvar.player.xpos, classvar.player.ypos)
        classvar.player.draw()
        maps.current_map.draw_foreground()
        conversations.currentconversation.draw()
    elif settings.state == "world":
        maps.current_map.draw(classvar.player.xpos, classvar.player.ypos)
        classvar.player.draw()
        maps.current_map.draw_foreground()
    elif settings.state == "battle":
        classvar.battle.draw()

    if (settings.menuonq):
        menu.draw()

    # put the screen on the widescreen
    pygame.draw.rect(variables.wide_screen, variables.BLACK, [0, 0, variables.mode[0], variables.mode[1]])
    variables.wide_screen.blit(variables.screen, [int(variables.mode[0] / 2 - variables.width / 2), 0])

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

    # add the past tick to the current time
    settings.current_time += clock.get_time()

# Close the window and quit, this is after the main loop has finished
pygame.quit()
