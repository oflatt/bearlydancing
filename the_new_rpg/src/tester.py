import pygame, os

# Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(16)


#master clock
clock = pygame.time.Clock()

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()
mode = modes[0]
height = mode[1]#displayinfo.current_h - 200
width = height #for not it is a square window
hh = height/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
wide_screen = pygame.display.set_mode(mode, pygame.FULLSCREEN)
screen = pygame.Surface([height, width])
running = True

print("starup time: " + str(pygame.time.get_ticks()) + " millis")
GR = {}
picnames = os.listdir(os.path.dirname(os.path.abspath("__file__")) + "/pics")

for x in picnames:
    p = 3
    nicename = x.replace(".png", "").lower()
    GR[nicename] = 3
print(GR)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(0)
    pygame.draw.rect(wide_screen, (200,200,200), [0,0,50,50])
    pygame.display.flip()
    clock.tick(60)