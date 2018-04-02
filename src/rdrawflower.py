import pygame, random

def makeflower():
    stemgreen = (66, 244, 131)
    flowerheight = random.choice([5, 6])
    flowerwidth = 5
    # stem 3-4 pixels tall, flower always the same
    s = pygame.Surface([5, flowerheight], pygame.SRCALPHA)

    ypos = flowerheight-1
    xpos = 2
    while ypos>1:
        s.set_at((xpos, ypos), stemgreen)
        if random.random() < 0.5:
            xpos += random.choice([-1, 1])
        if xpos > flowerwidth-2:
            xpos = flowerwidth-1
        elif xpos<1:
            xpos = 1
        ypos -= 1

    xpos -= 1
    # xpos now left pixel of flower
    if xpos > flowerwidth-3:
        xpos = flowerwidth-3
    elif xpos<0:
        xpos = 0
    
    # pick color of flower
    secondcolorbrightness = random.randint(0, 255)
    indexes = [0,1,2]
    # first index will be full brightness, the other will vary (the third rgb val will be 0)
    twoindexes = random.sample(indexes, 2)
    flowerpetalcolor = [0,0,0]
    flowerpetalcolor[twoindexes[0]] = 255
    flowerpetalcolor[twoindexes[1]] = random.randint(0, 255)
    # if it was green, don't let the petals just be green
    if twoindexes[0] == 1:
        if twoindexes[1] == 0:
            flowerpetalcolor[twoindexes[1]] = random.randint(180, 255)
        elif twoindexes[1] == 2:
            flowerpetalcolor[twoindexes[1]] = random.randint(170, 255)

    # top
    s.set_at((xpos+1, 0), flowerpetalcolor)
    s.set_at((xpos, 1), flowerpetalcolor) # left
    s.set_at((xpos+2, 1), flowerpetalcolor) # right
    s.set_at((xpos+1, 2), flowerpetalcolor) # bottom
    # center
    centerbrightness = random.randint(190, 255)
    s.set_at((xpos+1, 1), (centerbrightness, centerbrightness, 0))
    return s
