import variables, pygame

class Note():
    #if they miss the note or stop playing it halfway ison will turn false and they will miss the note
    ison = True

    beginning_score = None
    end_score = None
    pos = [0, 0]

    def __init__(self, value, time, duration):
        #value is the placement in the current scale (instrument) that the note is
        #time is time in the whole song it is
        self.value = value
        self.time = time
        self.duration = duration

    def draw(self, tempo):
        width = variables.width/20
        height = self.duration*tempo*variables.dancespeed
        #subtract height to y because the pos is the bottom of the rectangle
        if self.ison:
            color = variables.notes_colors[self.value-1]
        else:
            color = variables.GRAY

        end_height = variables.height/80

        p = self.pos
        #subtract height to y because the pos is the bottom of the rectangle
        pygame.draw.rect(variables.screen, color, [p[0], p[1]-height, width, height])
        pygame.draw.rect(variables.screen, color, [p[0]-width/8, p[1]-height, width*1.25, end_height])
        pygame.draw.rect(variables.screen, color, [p[0]-width/8, p[1]-end_height+2, width*1.25, end_height])