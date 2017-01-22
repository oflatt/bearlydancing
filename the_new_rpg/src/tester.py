import pygame, variables

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

wide_screen.fill(0)
w = font.render("ABCDEFGHIJKLMNOPQRSSSSS", 0, variables.BLUE)
wide_screen.blit(w, [0,100])
print(font.size("ABCDEFGHIJKLMNOPQRSSSSS"))
print(w.get_height())
wide_screen.fill(variables.WHITE, pygame.Rect(0, 100, 20, 37))

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)