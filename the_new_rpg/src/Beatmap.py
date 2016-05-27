import variables, pygame

padypos = variables.height*(3/4)
padxspace = variables.width/13

class Beatmap():
    scale = [50, 53, 55, 58, 60, 64, 68, 70] #list of eight pitches
    speed = 1
    starttime = 0
    #scores is a running list of the values for how well each note so far has been played (values for perfect, good ect)
    #it is cleared at every tradetime
    scores = []

    def __init__(self, tempo, notes, tradetimes):
        self.starttime = variables.current_time
        self.tempo = tempo
        #notes is an ordered list of Note, notes with earlier times first
        self.notes = notes
        self.tradetimes = tradetimes

    def draw(self):
        #draw the notes that are on the screen
        n = self.notes_on_screen()
        for x in range(0, len(n)):
            n[x].draw(self.notepos(n[x]), self.tempo)
        w = variables.width/20
        h = variables.height/80
        pygame.draw.rect(variables.screen, variables.notes_colors[0], [padxspace-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[1], [padxspace*2-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[2], [padxspace*3-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[3], [padxspace*4-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[4], [padxspace*5-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[5], [padxspace*6-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[6], [padxspace*7-w/8, padypos, w*1.25, h])
        pygame.draw.rect(variables.screen, variables.notes_colors[7], [padxspace*8-w/8, padypos, w*1.25, h])

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            checkednote = self.notes[x]
            if self.notepos(checkednote)[1] >= 0:
                n.insert(0, checkednote)
            else:
                break
        return n

    def notepos(self, note):
        #returns the pos of the bottom of the note
        dt = variables.current_time-self.starttime
        #ypos finds the notes place relative to pads then offsets it
        ypos = (dt-(note.time*self.tempo))*self.speed*variables.dancespeed
        xpos = note.value*padxspace
        return [xpos, ypos]

    def onkey(self, key):
        if key in variables.note1keys:
            print("ya")