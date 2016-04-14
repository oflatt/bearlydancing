#!/usr/bin/python
import pygame, variables, maps

from Player import Player
from Battle import Battle
import conversations, enemies

pygame.display.set_caption("theNewRpg")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
#pygame.mouse.set_visible(0)
player = Player(maps.current_map.startpoint[0], maps.current_map.startpoint[1])
battle = Battle(enemies.sheep, player)

def new_scale_offset():
    mapw = maps.current_map.finalimage.get_width()
    maph = maps.current_map.finalimage.get_height()
    if mapw<maph:
        smaller = mapw
    else:
        smaller = maph
    variables.scaleoffset = variables.width/smaller
    maps.current_map.scale_by_offset()
    player.scale_by_offset()

new_scale_offset()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_ESCAPE:
                done = True
            if variables.state == "conversation":
                conversations.currentconversation.keypress(event.key)
            else:
                player.keypress(event.key)

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            player.keyrelease(event.key)

    # --- Game Logic
    player.move()

    # --- Drawing Code
    variables.screen.fill(variables.WHITE)
    maps.current_map.draw(player.xpos, player.ypos)
    if variables.state == "conversation":
        conversations.currentconversation.draw()
        player.draw()
    elif variables.state == "world":
        player.draw()
    else:
        battle.draw()


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit, this is after the main loop has finished
pygame.quit()
