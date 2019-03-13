#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame, ctypes, os, time
 


# Setup
sample_rate = 22050
pygame.mixer.pre_init(sample_rate, 16, 2, 512)
pygame.mixer.init()
pygame.init()

import numpy

array = numpy.zeros((200, 2))
print(array.data)
a = pygame.mixer.Sound(buffer=array.data)
a.play()

print(pygame.key.name(273))

#master clock
clock = pygame.time.Clock()

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()

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

before = time.time()

for x in range(500):
    s = pygame.Surface((500, 500), pygame.SRCALPHA)

print("time 1 " + str(time.time()-before))

before = time.time()

s = pygame.Surface((500, 500), pygame.SRCALPHA)
s2 = pygame.Surface((500, 500), pygame.SRCALPHA)
for x in range(500):
    s.copy()
print("time 2 " + str(time.time()-before))

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


######
from colormath.color_objects import sRGBColor, HSLColor
c = sRGBColor(255, 0, 0, is_upscaled = True)
c2 = sRGBColor(0, 0, 255, is_upscaled = True)
from colormath import color_conversions
converted = color_conversions.convert_color(c, HSLColor)
converted2 = color_conversions.convert_color(c2, HSLColor)
print(converted.hsl_h)
print(converted2.hsl_h)
final = HSLColor((converted.hsl_h/2 + converted2.hsl_h/2), converted.hsl_s/2 + converted2.hsl_s/2, converted.hsl_l/2 + converted2.hsl_l/2)
print(final)
print(color_conversions.convert_color(final, sRGBColor))


#####

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
