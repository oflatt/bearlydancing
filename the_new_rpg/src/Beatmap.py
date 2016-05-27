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
    #list of whether the eight keys are held down or not
    held_keys = [False, False, False, False, False, False, False, False]

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
            n[x].draw(self.tempo)
        w = variables.width/20
        h = variables.height/80

        #draw which ones are pressed
        for x in range(0, 8):
            if self.held_keys[x] == True:
                ew = w*1.25
                pygame.draw.ellipse(variables.screen, variables.WHITE, [padxspace*(x+1)-w/8, padypos+h/2-ew/4, ew, ew/2])

        #draw bottom rectangles
        for x in range(1, 9):
            pygame.draw.rect(variables.screen, variables.notes_colors[x-1], [padxspace*(x)-w/8, padypos, w*1.25, h])

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            checkednote = self.notes[x]
            #update the pos of the note before putting it into the list
            checkednote.pos = self.notepos(checkednote)
            if checkednote.pos[1] >= 0:
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
            self.held_keys[0] = True
        elif key in variables.note2keys:
            self.held_keys[1] = True
        elif key in variables.note3keys:
            self.held_keys[2] = True
        elif key in variables.note4keys:
            self.held_keys[3] = True
        elif key in variables.note5keys:
            self.held_keys[4] = True
        elif key in variables.note6keys:
            self.held_keys[5] = True
        elif key in variables.note7keys:
            self.held_keys[6] = True
        elif key in variables.note8keys:
            self.held_keys[7] = True

    def onrelease(self, key):
        if key in variables.note1keys:
            self.held_keys[0] = False
        elif key in variables.note2keys:
            self.held_keys[1] = False
        elif key in variables.note3keys:
            self.held_keys[2] = False
        elif key in variables.note4keys:
            self.held_keys[3] = False
        elif key in variables.note5keys:
            self.held_keys[4] = False
        elif key in variables.note6keys:
            self.held_keys[5] = False
        elif key in variables.note7keys:
            self.held_keys[6] = False
        elif key in variables.note8keys:
            self.held_keys[7] = False