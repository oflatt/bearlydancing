import pygame, os
pygame.mixer.init()

s = pygame.mixer.Sound(os.path.join('sound', "C.wav"))
s.play()