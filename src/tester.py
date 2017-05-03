import pygame, variables, rdraw, play_sound

# Setup
pygame.init()

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
running = True

fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)

print("starup time: " + str(pygame.time.get_ticks()) + " millis")

loopl = play_sound.all_tones["sine"].loopbuffers[7]
max_sample = 2 ** (16 - 1) - 1
wheight = 400
print(max_sample)
for x in range(100):
    print(loopl[x][1])
    wide_screen.set_at((x, int((loopl[len(loopl)-(100-x)][1]/max_sample)*wheight+wheight+100)), (100,255,255))

for x in range(100):
    print(loopl[x][1])
    wide_screen.set_at((x+100, int((loopl[x][1]/max_sample)*wheight+wheight+100)), (255,255,255))

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)
