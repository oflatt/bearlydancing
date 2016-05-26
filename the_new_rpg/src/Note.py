import variables, pygame

class Note():
    def __init__(self, value, time, duration):
        #value is the placement in the current scale (instrument) that the note is
        #time is time in the whole song it is
        self.value = value
        self.time = time
        self.duration = duration

    def draw(self, pos, tempo):
        width = variables.width/20
        height = self.duration*tempo*variables.dancespeed
        #add height to y because the pos is the bottom of the rectangle
        pygame.draw.rect(variables.screen, variables.WHITE, [pos[0]+width/2, pos[1]-height, width, height])