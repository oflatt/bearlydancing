#!/usr/bin/python
import pygame, variables, maps

from Player import Player
from Battle import Battle
import conversations, classvar

pygame.display.set_caption("theNewRpg")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
#pygame.mouse.set_visible(0)

maps.new_scale_offset()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if variables.state == "conversation":
                conversations.currentconversation.keypress(event.key)
            elif variables.state == "world":
                classvar.player.keypress(event.key)
                maps.on_key(event.key)
            elif variables.state == "battle":
                classvar.battle.onkey(event.key)


        # User let up on a key
        elif event.type == pygame.KEYUP:
            if variables.state == "world":
                classvar.player.keyrelease(event.key)

    # --- Game Logic
    if variables.state == "world":
        classvar.player.move()
        maps.checkexit()
        maps.current_map.on_tick()
        maps.checkconversation()
    elif variables.state == "battle":
        classvar.battle.ontick()

    # --- Drawing Code
    variables.screen.fill(variables.WHITE)
    if variables.state == "conversation":
        conversations.currentconversation.draw()
        classvar.player.draw()
    elif variables.state == "world":
        maps.current_map.draw(classvar.player.xpos, classvar.player.ypos)
        classvar.player.draw()
        maps.current_map.draw_foreground()
    elif variables.state == "battle":
        classvar.battle.draw()

    #put the screen on the widescreen
    pygame.draw.rect(variables.wide_screen, variables.BLACK, [0,0, variables.mode[0], variables.mode[1]])
    variables.wide_screen.blit(variables.screen, [int(variables.mode[0]/2-variables.width/2), 0])

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

    #add the past tick to the current time
    variables.current_time += clock.get_time()

# Close the window and quit, this is after the main loop has finished
pygame.quit()
