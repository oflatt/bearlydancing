import graphics, pygame, variables, copy
from play_sound import stop_tone, play_tone, update_tone
from variables import padypos

padxspace = variables.width / 12
padheight = variables.height / 80
middleoffset = padxspace / 2

class Beatmap():

    def __init__(self, tempo, notes):
        self.starttime = variables.settings.current_time
        # tempo in how many milliseconds per beat.
        self.tempo = tempo
        self.originalnotes = notes
        # notes is an ordered list of Note, notes with earlier times first
        self.notes = notes
        self.scale = [2, 2, 1, 2, 2, 2, 1]  # list of offsets for the scale
        self.speed = 1
        self.starttime = 0
        self.pausetime = 0
        # scores is a running list of the values for how well each note so far has been played. values for perfect, ect
        self.scores = []
        # held keys is None if the key is not held, and the tone if it is held
        self.held_keys = [None, None, None, None, None, None, None, None]
        self.time_key_started = [0, 0, 0, 0, 0, 0, 0, 0]
        # when to stop displaying the text, in milliseconds
        self.feedback_timers = [0, 0, 0, 0, 0, 0, 0, 0]
        # list of text pics to display for each note (perfect ect.)
        self.feedback = [graphics.Atext, graphics.Stext, graphics.Dtext, graphics.Ftext,
            graphics.Jtext, graphics.Ktext, graphics.Ltext, graphics.SEMICOLONtext]

    def pause(self):
        self.pausetime = variables.settings.current_time

    def unpause(self):
        self.starttime += variables.settings.current_time - self.pausetime
        self.pausetime = 0

    def reset(self, battlestarttime, beginningq):
        self.scores = []
        synctime = (variables.settings.current_time - battlestarttime) % self.tempo
        self.starttime = variables.settings.current_time - synctime
        if (beginningq):
            fsl = self.starttime + 4000
            self.feedback_timers = [fsl, fsl, fsl, fsl, fsl, fsl, fsl, fsl]
            self.feedback = [graphics.Atext, graphics.Stext, graphics.Dtext, graphics.Ftext,
                             graphics.Jtext, graphics.Ktext, graphics.Ltext, graphics.SEMICOLONtext]
        self.notes = copy.deepcopy(self.originalnotes)

    def draw(self):
        w = variables.width / 20
        # draw which ones are pressed
        for x in range(0, 8):
            if self.held_keys[x] != None:
                xoffset = 0
                if (x + 1 > 4):
                    xoffset = middleoffset
                ew = w * 1.25
                pygame.draw.ellipse(variables.screen, variables.WHITE, [padxspace * (x + 1) - w / 8 + xoffset,
                                                                        padypos - padheight + padheight / 2 - ew / 4,
                                                                        ew, ew / 2])
        # draw the notes that are on the screen
        n = self.notes_on_screen()
        for x in range(0, len(n)):
            n[x].draw(self.tempo)
        
        self.draw_pads()

    def draw_pads(self):
        w = variables.width / 20
        # draw bottom rectangles
        for x in range(1, 9):
            xoffset = 0
            if (x > 4):
                xoffset = middleoffset
            pygame.draw.rect(variables.screen, variables.notes_colors[x - 1],
                             [padxspace * (x) - w / 8 + xoffset, padypos - padheight, w * 1.25, padheight])

        # draw the feedback (keys then scores, perfect ect)
        for x in range(0, 8):
            xoffset = 0
            if (x > 3):
                xoffset = middleoffset
            if variables.settings.current_time < self.feedback_timers[x]:
                variables.screen.blit(self.feedback[x], [padxspace * (x + 1) - w / 8 + xoffset, padypos - padheight])

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            # update the pos of the note
            self.notes[x].pos = self.notepos(self.notes[x])
            checkednote = self.notes[x]
            if checkednote.pos[1] >= 0:
                n.insert(0, checkednote)
            else:
                break
        return n

    def notepos(self, note):
        # returns the pos of the bottom of the note
        dt = variables.settings.current_time - self.starttime
        if (self.pausetime):
            dt -= variables.settings.current_time - self.pausetime

        ypos = (dt - (note.time * self.tempo)) * self.speed * variables.dancespeed
        if (note.screenvalue > 3):
            xpos = note.screenvalue * padxspace + middleoffset + padxspace
        else:
            xpos = note.screenvalue * padxspace + padxspace
        return [xpos, ypos]

    def pos_to_score(self, ypos):
        difference = abs(ypos - padypos)
        if difference <= variables.perfect_range:
            return variables.perfect_value
        elif difference <= variables.good_range:
            return variables.good_value
        elif difference <= variables.ok_range:
            return variables.ok_value
        elif difference <= variables.miss_range:
            return variables.miss_value
        else:
            return None

    def get_note_place_from_value_begin(self, v):
        np = None
        notevalue = v
        for x in range(0, len(self.notes)):
            if self.notes[x].screenvalue == v and self.notes[x].ison and self.notes[x].beginning_score == None:
                np = x
                notevalue = self.notes[x].value
                break
        return [np, notevalue]

    def get_note_place_from_value_end(self, v):
        np = None
        for x in range(0, len(self.notes)):
            if self.notes[x].screenvalue == v and self.notes[x].ison and self.notes[x].end_score == None:
                np = x
                break
        return np

    def onkey(self, key):
        def check_note(np):
            if self.notes[np].beginning_score == None:
                s = self.pos_to_score(self.notes[np].pos[1] - padheight)
                if s != None:
                    self.notes[np].beginning_score = s
                    if self.notes[np].beginning_score == variables.miss_value:
                        self.notes[np].ison = False
                        self.feedback[self.notes[np].screenvalue] = graphics.MISStext
                        self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo

        # returns the value for the sound produced
        def check_place(v):
            placeandvalue = self.get_note_place_from_value_begin(v)
            np = placeandvalue[0]
            if not np == None:
                check_note(np)
            return placeandvalue[1]

        def simple_value_in_key(v):
            av = abs(v)
            sound_value = 0
            if (v < 0):
                for x in range(av):
                    sound_value -= self.scale[6 - (x % 7)]
            else:
                for x in range(av):
                    sound_value += self.scale[x % 7]
            return sound_value

        def playnotepressed(kp):
            v = check_place(kp)
            v = simple_value_in_key(v)
            self.held_keys[kp] = v
            self.time_key_started[kp] = variables.settings.current_time
            play_tone(v)

        if key in variables.settings.note1keys:
            playnotepressed(0)
        elif key in variables.settings.note2keys:
            playnotepressed(1)
        elif key in variables.settings.note3keys:
            playnotepressed(2)
        elif key in variables.settings.note4keys:
            playnotepressed(3)
        elif key in variables.settings.note5keys:
            playnotepressed(4)
        elif key in variables.settings.note6keys:
            playnotepressed(5)
        elif key in variables.settings.note7keys:
            playnotepressed(6)
        elif key in variables.settings.note8keys:
            playnotepressed(7)

    def onrelease(self, key):

        def check_note(np):
            if self.notes[np].end_score == None and self.notes[np].beginning_score != None:
                top_of_note = self.notes[np].pos[1] - self.notes[np].height(self.tempo)
                s = self.pos_to_score(top_of_note)

                if s == None and self.notes[np].beginning_score != None:
                    s = variables.miss_value
                    self.notes[np].height_offset = self.notes[np].pos[1] - padypos

                if s != None:
                    if s < self.notes[np].beginning_score:
                        final_note_score = s
                    else:
                        final_note_score = self.notes[np].beginning_score

                    self.notes[np].end_score = s

                    if s == variables.miss_value:
                        self.notes[np].height_offset = self.notes[np].pos[1] - padypos
                        self.notes[np].ison = False

                    self.scores.append(final_note_score)

                    if final_note_score == variables.miss_value:
                        self.feedback[self.notes[np].screenvalue] = graphics.MISStext
                        self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.good_value:
                        self.feedback[self.notes[np].screenvalue] = graphics.GOODtext
                        self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.ok_value:
                        self.feedback[self.notes[np].screenvalue] = graphics.OKtext
                        self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.perfect_value:
                        self.feedback[self.notes[np].screenvalue] = graphics.PERFECTtext
                        self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo
            # released before a note, penalty for randomly playing notes not written
            else:
                self.scores.append(variables.miss_value)
                self.feedback[self.notes[np].screenvalue] = graphics.MISStext
                self.feedback_timers[self.notes[np].screenvalue] = variables.settings.current_time + self.tempo

        def check_place(v):
            np = self.get_note_place_from_value_end(v)
            if not np == None:
                check_note(np)
            else:
                self.scores.append(variables.miss_value)
                self.feedback[v] = graphics.MISStext
                self.feedback_timers[v] = variables.settings.current_time + self.tempo

        if key in variables.settings.note1keys:
            check_place(0)
            stop_tone(self.held_keys[0])
            self.held_keys[0] = None
        elif key in variables.settings.note2keys:
            check_place(1)
            stop_tone(self.held_keys[1])
            self.held_keys[1] = None
        elif key in variables.settings.note3keys:
            check_place(2)
            stop_tone(self.held_keys[2])
            self.held_keys[2] = None
        elif key in variables.settings.note4keys:
            check_place(3)
            stop_tone(self.held_keys[3])
            self.held_keys[3] = None
        elif key in variables.settings.note5keys:
            check_place(4)
            stop_tone(self.held_keys[4])
            self.held_keys[4] = None
        elif key in variables.settings.note6keys:
            check_place(5)
            stop_tone(self.held_keys[5])
            self.held_keys[5] = None
        elif key in variables.settings.note7keys:
            check_place(6)
            stop_tone(self.held_keys[6])
            self.held_keys[6] = None
        elif key in variables.settings.note8keys:
            check_place(7)
            stop_tone(self.held_keys[7])
            self.held_keys[7] = None

    def ontick(self):
        # remove notes that are off the screen
        np = 0
        while np < len(self.notes):
            if self.notes[np].pos[1] - self.notes[np].height(self.tempo) > variables.height:
                del self.notes[0]
            else:
                break

        # make the notes not played a miss
        for x in range(len(self.notes)):
            # find whether the miss range or the distance to middle of note is smaller
            h = self.notes[x].height(self.tempo)
            smaller = variables.smaller(h / 2, variables.miss_range)

            if self.notes[x].pos[1] - smaller > padypos and self.notes[x].beginning_score == None:
                if self.notes[x].ison:
                    self.feedback[self.notes[x].screenvalue] = graphics.MISStext
                    self.feedback_timers[self.notes[x].screenvalue] = variables.settings.current_time + self.tempo
                    self.notes[x].ison = False
                    self.scores.append(variables.miss_value)
                elif self.notes[x].pos[1] < 0:
                    # if you are in a part of the list before the screen, don't keep checking
                    # (assuming the list of notes must be ordered by time, of course)
                    break

        # update played notes for looping
        for k in self.held_keys:
            if not k == None:
                update_tone(k)

    def reset_buttons(self):
        for x in range(8):
            self.held_keys[x] = None
        # turn off sound
        for x in range(-24, 24):
            stop_tone(x)
