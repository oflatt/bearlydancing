import pygame

class Settings():
    # keybindings
    upkeys = [pygame.K_UP, pygame.K_w]
    downkeys = [pygame.K_DOWN, pygame.K_s]
    leftkeys = [pygame.K_LEFT, pygame.K_a]
    rightkeys = [pygame.K_RIGHT, pygame.K_d]
    enterkeys = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
    note1keys = [pygame.K_a]
    note2keys = [pygame.K_s]
    note3keys = [pygame.K_d]
    note4keys = [pygame.K_f]
    note5keys = [pygame.K_j]
    note6keys = [pygame.K_k]
    note7keys = [pygame.K_l]
    note8keys = [pygame.K_SEMICOLON]

    # state can be world, battle, or conversation
    state = "world"
    menuonq = False
    easymodeq = False

    # master clock
    current_time = 0
