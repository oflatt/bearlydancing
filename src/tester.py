import pygame, ctypes, os

# Setup
pygame.init()

#master clock
clock = pygame.time.Clock()

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()
ctypes.windll.user32.SetProcessDPIAware()
mode = modes[0]
height = mode[1]#displayinfo.current_h - 200
width = mode[0]
hh = height/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
wide_screen = pygame.display.set_mode(mode, flags)
running = True

fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)

print("starup time: " + str(pygame.time.get_ticks()) + " millis")

def sscale(img):
    factor = 0.0025 #This basically determines how much of the map we can see
    w = img.get_width()
    h = img.get_height()
    endsize = height*factor
    if w > h:
        smaller = h
    else:
        smaller = w
    return pygame.transform.scale(img, [int((w/smaller)*endsize*smaller), int((h/smaller)*endsize*smaller)])

bigpic = pygame.image.load(os.path.join('pics', "randomgrassland0.png")).convert_alpha()
#bigpic = sscale(bigpic)

bigpics = [bigpic.subsurface([0,0,int(bigpic.get_width()/2), bigpic.get_height()]),
           bigpic.subsurface([int(bigpic.get_width()/2),0,int(bigpic.get_width()/2), bigpic.get_height()])]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    wide_screen.fill((0,0,0))
    #wide_screen.blit(bigpic, [0,0])
    #pygame.transform.scale(wide_screen, [80, 80])
    hpic = pygame.image.load(os.path.join('pics', "honeyside0.png")).convert_alpha()
    wide_screen.blit(pygame.transform.scale(hpic, [hpic.get_width()*10, hpic.get_height()*10]), [0,0])

    wide_screen.blit(font.render(str(clock.get_fps()), 0, (255,255,255)), [20, 20])
                
    pygame.display.flip()

    clock.tick(240)
