import variables, pygame, graphics
from variables import padypos

padxspace = variables.width/13
padheight = variables.width/80

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
    feedback = [graphics.Atext, graphics.Stext, graphics.Dtext, graphics.Ftext,
                graphics.Jtext, graphics.Ktext, graphics.Ltext, graphics.SEMICOLONtext]
    #when to stop displaying the text, in milliseconds
    feedback_timers = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, tempo, notes, tradetimes):
        self.starttime = variables.current_time
        self.tempo = tempo
        #notes is an ordered list of Note, notes with earlier times first
        self.notes = notes
        self.tradetimes = tradetimes
        fsl = self.starttime+4000
        self.feedback_timers = [fsl, fsl, fsl, fsl, fsl, fsl, fsl, fsl]

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
            pygame.draw.rect(variables.screen, variables.notes_colors[x-1], [padxspace*(x)-w/8, padypos, w*1.25, padheight])

        #draw the feedback (keys then scores, perfect ect)
        for x in range(0, 8):
            if variables.current_time < self.feedback_timers[x]:
                variables.screen.blit(self.feedback[x], [padxspace*(x+1)-w/8, padypos+h*3])

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

    def pos_to_score(self, ypos):
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
                return None

    def get_note_place_from_value(self, v):
            np = None
            for x in range(0, len(self.notes)):
                if self.notes[x].value == v and self.notes[x].ison:
                    np = x
                    break
            return np

    def onkey(self, key):
        print("down")
        print(self.notes[4].beginning_score)
        print(self.notes[4].end_score)

        def check_note(np):
            if self.notes[np].beginning_score == None:
                s = self.pos_to_score(self.notes[np].pos[1]-padheight)
                if s != None:
                    self.notes[np].beginning_score = s
                    if self.notes[np].beginning_score == variables.miss_value:
                        self.notes[np].ison = False

        def check_place(v):
            np = self.get_note_place_from_value(v)
            if not np == None:
                check_note(np)

        if key in variables.note1keys:
            check_place(1)
            self.held_keys[0] = True
        elif key in variables.note2keys:
            check_place(2)
            self.held_keys[1] = True
        elif key in variables.note3keys:
            check_place(3)
            self.held_keys[2] = True
        elif key in variables.note4keys:
            check_place(4)
            self.held_keys[3] = True
        elif key in variables.note5keys:
            check_place(5)
            self.held_keys[4] = True
        elif key in variables.note6keys:
            check_place(6)
            self.held_keys[5] = True
        elif key in variables.note7keys:
            check_place(7)
            self.held_keys[6] = True
        elif key in variables.note8keys:
            check_place(8)
            self.held_keys[7] = True

    def onrelease(self, key):
        print("up")
        print(self.notes[4].beginning_score)
        print(self.notes[4].end_score)

        def check_note(np):
            if self.notes[np].end_score == None and self.notes[np].beginning_score != None:
                s = self.pos_to_score(self.notes[np].pos[1]-self.notes[np].height(self.tempo))

                if s != None:
                    if s < self.notes[np].beginning_score:
                        end_score = s
                    else:
                        end_score = self.notes[np].beginning_score

                    self.notes[np].end_score = s

                    if s == variables.miss_value:
                        self.notes[np].ison = False

                    self.scores.append(end_score)

                    if end_score == variables.miss_value:
                        self.feedback[self.notes[np].value-1] = graphics.MISStext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif end_score == variables.good_value:
                        self.feedback[self.notes[np].value-1] = graphics.GOODtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif end_score == variables.ok_value:
                        self.feedback[self.notes[np].value-1] = graphics.OKtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif end_score == variables.perfect_value:
                        self.feedback[self.notes[np].value-1] = graphics.PERFECTtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo

        def check_place(v):
            np = self.get_note_place_from_value(v)
            if not np == None:
                check_note(np)

        if key in variables.note1keys:
            check_place(1)
            self.held_keys[0] = False
        elif key in variables.note2keys:
            check_place(2)
            self.held_keys[1] = False
        elif key in variables.note3keys:
            check_place(3)
            self.held_keys[2] = False
        elif key in variables.note4keys:
            check_place(4)
            self.held_keys[3] = False
        elif key in variables.note5keys:
            check_place(5)
            self.held_keys[4] = False
        elif key in variables.note6keys:
            check_place(6)
            self.held_keys[5] = False
        elif key in variables.note7keys:
            check_place(7)
            self.held_keys[6] = False
        elif key in variables.note8keys:
            check_place(8)
            self.held_keys[7] = False