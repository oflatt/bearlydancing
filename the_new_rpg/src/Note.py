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
        #subtract height to y because the pos is the bottom of the rectangle
        pygame.draw.rect(variables.screen, variables.notes_colors[self.value-1], [pos[0], pos[1]-height, width, height])
        pygame.draw.rect(variables.screen, variables.notes_colors[self.value-1], [pos[0]-width/8, pos[1]-height, width*1.25, variables.height/80])
        pygame.draw.rect(variables.screen, variables.notes_colors[self.value-1], [pos[0]-width/8, pos[1]-variables.height/80, width*1.25, variables.height/80])