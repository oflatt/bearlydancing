import variables, pygame, graphics
from variables import padypos

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
    #list of the notes on the screen currently
    nos = []
    #list of text pics to display for each note (perfect ect.)
    feedback = [None, None, None, None, None, None, None, None]
    feedback_timers = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, tempo, notes, tradetimes):
        self.starttime = variables.current_time
        self.tempo = tempo
        #notes is an ordered list of Note, notes with earlier times first
        self.notes = notes
        self.tradetimes = tradetimes

    def draw(self):
        #draw the notes that are on the screen
        self.nos = self.notes_on_screen()
        n = self.nos
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

        #draw the keys
        variables.screen.blit(graphics.Atext, [padxspace-w/8, padypos+h*3])
        variables.screen.blit(graphics.Stext, [padxspace*2-w/8, padypos+h*3])
        variables.screen.blit(graphics.Dtext, [padxspace*3-w/8, padypos+h*3])
        variables.screen.blit(graphics.Ftext, [padxspace*4-w/8, padypos+h*3])
        variables.screen.blit(graphics.Jtext, [padxspace*5-w/8, padypos+h*3])
        variables.screen.blit(graphics.Ktext, [padxspace*6-w/8, padypos+h*3])
        variables.screen.blit(graphics.Ltext, [padxspace*7-w/8, padypos+h*3])
        variables.screen.blit(graphics.SEMICOLONtext, [padxspace*8-w/8, padypos+h*3])

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            self.notes[x].pos = self.notepos(self.notes[x])
            checkednote = self.notes[x]
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
        def get_note_place_from_value(v):
            np = False
            for x in range(0, len(self.nos)):
                if self.notes[x].value == v and self.notes[x].ison:
                    np = x
                    break
            return np

        def pos_to_score(ypos):
            difference = abs(ypos-padypos)
            if difference <= variables.perfect_range:
                return variables.perfect_value
            elif difference <= variables.good_range:
                return variables.good_value
            elif difference<= variables.ok_range:
                return variables.ok_value
            elif difference<= variables.miss_range:
                return variables.miss_value
            else:
                return False

        def check_note(np):
            if self.notes[np].beginning_score == None:
                s = pos_to_score(self.notes[np].pos[1])
                if s:
                    self.notes[np].beginning_score = s


        if key in variables.note1keys:
            np = get_note_place_from_value(1)
            if np:
                check_note(np)
            self.held_keys[0] = True
        elif key in variables.note2keys:
            np = get_note_place_from_value(2)
            if np:
                check_note(np)
            self.held_keys[1] = True
        elif key in variables.note3keys:
            np = get_note_place_from_value(3)
            if np:
                check_note(np)
            self.held_keys[2] = True
        elif key in variables.note4keys:
            np = get_note_place_from_value(4)
            if np:
                check_note(np)
            self.held_keys[3] = True
        elif key in variables.note5keys:
            np = get_note_place_from_value(5)
            if np:
                check_note(np)
            self.held_keys[4] = True
        elif key in variables.note6keys:
            np = get_note_place_from_value(6)
            if np:
                check_note(np)
            self.held_keys[5] = True
        elif key in variables.note7keys:
            np = get_note_place_from_value(7)
            if np:
                check_note(np)
            self.held_keys[6] = True
        elif key in variables.note8keys:
            np = get_note_place_from_value(8)
            if np:
                check_note(np)
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