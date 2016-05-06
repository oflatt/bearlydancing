import variables, pygame

class Note():
    def __init__(self, value, time):
        #value is the placement in the current scale (instrument) that the note is
        #time is time in the whole song it is
        self.value = value
        self.time = time

    def draw(self, pos):
        width = variables.width/20
        pygame.draw.ellipse(variables.screen, variables.WHITE, [pos[0], pos[1], width, width])