#!/usr/bin/python
import pygame, variables, maps

from Player import Player

pygame.display.set_caption("theNewRpg")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
#pygame.mouse.set_visible(0)

#variables
player = Player(maps.current_map.startpoint[0], maps.current_map.startpoint[1])

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
    player.draw()


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit, this is after the main loop has finished
pygame.quit()
