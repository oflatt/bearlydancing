import pygame

class Settings():
    # keybindings
    keylist = ["up","down","left","right","action","note1","note2","note3","note4","note5","note6","note7","note8", "pause/menu"]
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
    escapekeys = [pygame.K_ESCAPE]

    # state can be world, battle, or conversation
    state = "world"
    backgroundstate = "world"
    menuonq = True
    easymodeq = False
    #possible soundpacks can be seen by listing the keys in all_sounds in play_sound
    soundpack = "sine"

    username = "Greg"
    bearname = "Honey"

    # master clock
    current_time = 0

    # this is an offset for all enemy levels
    difficulty = 0
