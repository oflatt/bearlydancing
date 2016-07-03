import variables, pygame, graphics
from variables import padypos
from play_sound import play_sound, stop_sound

padxspace = variables.width/12
padheight = variables.width/80
middleoffset = padxspace/2

class Beatmap():
    scale = ['C', 'D', 'E', 'F','G', 'A', 'B', 'Chigh'] #list of eight notes
    speed = 1
    starttime = 0
    #scores is a running list of the values for how well each note so far has been played (values for perfect, good ect)
    scores = []
    #list of whether the eight keys are held down or not
    held_keys = [False, False, False, False, False, False, False, False]
    #list of text pics to display for each note (perfect ect.)
    feedback = [graphics.Atext, graphics.Stext, graphics.Dtext, graphics.Ftext,
                graphics.Jtext, graphics.Ktext, graphics.Ltext, graphics.SEMICOLONtext]
    #when to stop displaying the text, in milliseconds
    feedback_timers = [0, 0, 0, 0, 0, 0, 0, 0]
    drumcounter = 0

    def __init__(self, tempo, notes):
        self.starttime = variables.current_time
        self.tempo = tempo
        #notes is an ordered list of Note, notes with earlier times first
        self.notes = notes
        fsl = self.starttime+4000
        self.feedback_timers = [fsl, fsl, fsl, fsl, fsl, fsl, fsl, fsl]

    def reset(self):
        self.drumcounter = 0
        self.starttime = variables.current_time
        fsl = self.starttime+4000
        self.feedback_timers = [fsl, fsl, fsl, fsl, fsl, fsl, fsl, fsl]
        self.feedback = [graphics.Atext, graphics.Stext, graphics.Dtext, graphics.Ftext,
                         graphics.Jtext, graphics.Ktext, graphics.Ltext, graphics.SEMICOLONtext]


    def draw(self):
        #print(str(self.notes[0].pos[1]) + " " + str(self.notes[0].time) + " " + str(self.notes[0].end_score))

        #draw the notes that are on the screen
        n = self.notes_on_screen()
        for x in range(0, len(n)):
            n[x].draw(self.tempo)
        w = variables.width/20

        #draw which ones are pressed
        for x in range(0, 8):
            if self.held_keys[x] == True:
                xoffset = 0
                if(x+1 > 4):
                    xoffset = middleoffset
                ew = w*1.25
                pygame.draw.ellipse(variables.screen, variables.WHITE, [padxspace*(x+1)-w/8+xoffset,
                                                                        padypos+padheight/2-ew/4, ew, ew/2])

        self.draw_pads()

    def draw_pads(self):
        w = variables.width/20
        #draw bottom rectangles
        for x in range(1, 9):
            xoffset = 0
            if (x>4):
                xoffset = middleoffset
            pygame.draw.rect(variables.screen, variables.notes_colors[x-1], [padxspace*(x)-w/8+xoffset, padypos, w*1.25, padheight])

        #draw the feedback (keys then scores, perfect ect)
        for x in range(0, 8):
            xoffset = 0
            if (x>3):
                xoffset = middleoffset
            if variables.current_time < self.feedback_timers[x]:
                variables.screen.blit(self.feedback[x], [padxspace*(x+1)-w/8+xoffset, padypos])

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            #update the pos of the note
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
        if(note.value>4):
            xpos = note.value*padxspace + middleoffset
        else:
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

    def get_note_place_from_value_begin(self, v):
            np = None
            for x in range(0, len(self.notes)):
                if self.notes[x].value == v and self.notes[x].ison and self.notes[x].beginning_score == None:
                    np = x
                    break
            return np

    def get_note_place_from_value_end(self, v):
            np = None
            for x in range(0, len(self.notes)):
                if self.notes[x].value == v and self.notes[x].ison:
                    np = x
                    break
            return np

    def onkey(self, key):
        def check_note(np):
            if self.notes[np].beginning_score == None:
                s = self.pos_to_score(self.notes[np].pos[1]-padheight)
                if s != None:
                    self.notes[np].beginning_score = s
                    if self.notes[np].beginning_score == variables.miss_value:
                        self.notes[np].ison = False
                        self.feedback[self.notes[np].value-1] = graphics.MISStext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo

        def check_place(v):
            np = self.get_note_place_from_value_begin(v)
            if not np == None:
                check_note(np)

        if key in variables.note1keys:
            check_place(1)
            self.held_keys[0] = True
            play_sound(self.scale[0])
        elif key in variables.note2keys:
            check_place(2)
            self.held_keys[1] = True
            play_sound(self.scale[1])
        elif key in variables.note3keys:
            check_place(3)
            self.held_keys[2] = True
            play_sound(self.scale[2])
        elif key in variables.note4keys:
            check_place(4)
            self.held_keys[3] = True
            play_sound(self.scale[3])
        elif key in variables.note5keys:
            check_place(5)
            self.held_keys[4] = True
            play_sound(self.scale[4])
        elif key in variables.note6keys:
            check_place(6)
            self.held_keys[5] = True
            play_sound(self.scale[5])
        elif key in variables.note7keys:
            check_place(7)
            self.held_keys[6] = True
            play_sound(self.scale[6])
        elif key in variables.note8keys:
            check_place(8)
            self.held_keys[7] = True
            play_sound(self.scale[7])

    def onrelease(self, key):

        def check_note(np):
            if self.notes[np].end_score == None and self.notes[np].beginning_score != None:
                top_of_note = self.notes[np].pos[1]-self.notes[np].height(self.tempo)
                s = self.pos_to_score(top_of_note)

                if s == None and self.notes[np].beginning_score != None:
                    s = variables.miss_value
                    self.notes[np].height_offset = self.notes[np].pos[1]-padypos

                if s != None:
                    if s < self.notes[np].beginning_score:
                        final_note_score = s
                    else:
                        final_note_score = self.notes[np].beginning_score

                    self.notes[np].end_score = s

                    if s == variables.miss_value:
                        self.notes[np].height_offset = self.notes[np].pos[1]-padypos
                        self.notes[np].ison = False

                    self.scores.append(final_note_score)

                    if final_note_score == variables.miss_value:
                        self.feedback[self.notes[np].value-1] = graphics.MISStext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif final_note_score == variables.good_value:
                        self.feedback[self.notes[np].value-1] = graphics.GOODtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif final_note_score == variables.ok_value:
                        self.feedback[self.notes[np].value-1] = graphics.OKtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo
                    elif final_note_score == variables.perfect_value:
                        self.feedback[self.notes[np].value-1] = graphics.PERFECTtext
                        self.feedback_timers[self.notes[np].value-1] = variables.current_time+self.tempo

        def check_place(v):
            np = self.get_note_place_from_value_end(v)
            if not np == None:
                check_note(np)

        if key in variables.note1keys:
            check_place(1)
            self.held_keys[0] = False
            stop_sound(self.scale[0])
        elif key in variables.note2keys:
            check_place(2)
            self.held_keys[1] = False
            stop_sound(self.scale[1])
        elif key in variables.note3keys:
            check_place(3)
            self.held_keys[2] = False
            stop_sound(self.scale[2])
        elif key in variables.note4keys:
            check_place(4)
            self.held_keys[3] = False
            stop_sound(self.scale[3])
        elif key in variables.note5keys:
            check_place(5)
            self.held_keys[4] = False
            stop_sound(self.scale[4])
        elif key in variables.note6keys:
            check_place(6)
            self.held_keys[5] = False
            stop_sound(self.scale[5])
        elif key in variables.note7keys:
            check_place(7)
            self.held_keys[6] = False
            stop_sound(self.scale[6])
        elif key in variables.note8keys:
            check_place(8)
            self.held_keys[7] = False
            stop_sound(self.scale[7])

    def ontick(self):
        #remove notes that are off the screen
        np = 0
        while np < len(self.notes):
            if self.notes[np].pos[1]-self.notes[np].height(self.tempo) > variables.height:
                del self.notes[0]
            else:
                break

        #make the notes not played a miss
        for x in range(len(self.notes)):
            #find whether the miss range or the distance to middle of note is smaller
            h = self.notes[x].height(self.tempo)
            smaller = variables.smaller(h/2, variables.miss_range)

            if self.notes[x].pos[1]-smaller>padypos and self.notes[x].beginning_score == None:
                if self.notes[x].ison:
                    self.feedback[self.notes[x].value-1] = graphics.MISStext
                    self.feedback_timers[self.notes[x].value-1] = variables.current_time+self.tempo
                    self.notes[x].ison = False
                    self.scores.append(variables.miss_value)
                elif self.notes[x].pos[1]<0:
                    #if you are in a part of the list before the screen, don't keep checking
                    #(assuming the list of notes must be ordered by time, of course)
                    break

        dt = variables.current_time-self.starttime
        ypos = (dt-(self.drumcounter*self.tempo))*self.speed*variables.dancespeed
        #play a drum sound if it is on the beat
        if(ypos >= padypos):
            self.drumcounter += 1
            play_sound("drum kick heavy")


    def reset_buttons(self):
        for x in range(8):
            self.held_keys[x] = False
        #turn off sound
        for x in range(8):
            stop_sound(self.scale[x])