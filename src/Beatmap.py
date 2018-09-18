import graphics, pygame, variables, copy
from play_sound import stop_tone, play_tone, update_tone, play_effect
from pygame import Rect

padxspace = variables.width / 12
padheight = variables.height / 80
middleoffset = padxspace / 2

class Beatmap():

    def __init__(self, tempo, notes):
        # tempo in how many milliseconds per beat.
        self.tempo = tempo
        self.originalnotes = notes
        
        # notes is an ordered list of Note, notes with earlier times first
        self.notes = copy.deepcopy(self.originalnotes)
        self.scale = [2, 2, 1, 2, 2, 2, 1]  # list of offsets for the scale
        self.speed = 1 # unused currently
        self.starttime = 0
        self.pausetime = 0

        # scores is a running list of the values for how well each note so far has been played. values for perfect, ect
        self.scores = []
        # held keys is None if the key is not held, and the tone if it is held
        self.held_keys = [None] * 8
        # spaceheldq stores if the modifier key (default space) is currently being held
        self.spacepressedp = False
        self.time_key_started = [0] * 8
        # when to stop displaying the text, in milliseconds
        self.feedback_timers = [None] * 8
        self.feedback = []
        self.setfeedbacktocontrols()

        self.drumcounter = 0

    def setfeedbacktocontrols(self):
        self.feedback = []
        for x in range(8):
            n = pygame.key.name(variables.settings.keydict["note" + str(x+1)][0])
            self.feedback.append(n)

    def pause(self):
        self.pausetime = variables.settings.current_time

    def unpause(self):
        self.starttime += variables.settings.current_time - self.pausetime
        self.pausetime = 0

    def showkeys(self):
        self.feedback_timers = [None] * 8
        self.setfeedbacktocontrols()


    def reset(self, battlestarttime, beginningq):
        self.scores = []
        synctime = self.tempo - ((variables.settings.current_time - battlestarttime) % self.tempo)
        self.starttime = variables.settings.current_time + synctime
        self.showkeys()
        if not beginningq:
            self.notes = copy.deepcopy(self.originalnotes)
        self.drumcounter = 0

    def draw(self):
        w = variables.width / 20
        ew = w * 1.25
        padellipseypos = variables.getpadypos() - padheight + padheight / 2 - ew / 4
        padcolor = (180, 180, 180)
        if self.spacepressedp:
            padcolor = (variables.PINK[0]-70, variables.PINK[1]-30, variables.PINK[2]-70)
        
        # draw which ones are pressed
        for x in range(0, 8):
            if self.held_keys[x] != None:
                xoffset = 0
                if (x + 1 > 4):
                    xoffset = middleoffset
                expos = padxspace * (x + 1) - w / 8 + xoffset
                pygame.draw.ellipse(variables.screen, padcolor, [expos,
                                                                        padellipseypos,
                                                                        ew, ew / 2])
                variables.dirtyrects.append(Rect(expos, padellipseypos, ew, ew/2))
        # draw the notes that are on the screen
        for n in self.notes:
            n.draw(self.tempo)
        
        self.draw_pads()

        # also draw notetime to top left
        if variables.devmode:
            notetimetext = variables.font.render(str(self.notetime()), 0, variables.WHITE)
            variables.screen.blit(notetimetext, [10, 2*variables.font.get_linesize()])

    def getfeedbackpic(self, index):
        s = self.feedback[index]
        rotatep = False
        if s == "miss":
            s = "MISS"
            rotatep = True
        elif s == "ok":
            rotatep = True
            s = "OK"
        elif s == "good":
            s = "GOOD"
            rotatep = True
        elif s == "perfect":
            s = "PERFECT"
            rotatep = True
        pic = graphics.getTextPic(s, variables.gettextsize(), variables.WHITE)
        if rotatep:
            pic = pygame.transform.rotate(pic, -45)
        return pic
            
    def draw_pads(self):
        w = variables.width / 20
        # draw bottom rectangles
        for x in range(1, 9):
            xoffset = 0
            if (x > 4):
                xoffset = middleoffset
            padcolor = variables.notes_colors[x-1]
            if(self.spacepressedp):
                padcolor = variables.PINK
            # draw the pads
            padrect = Rect(padxspace * (x) - w / 8 + xoffset, variables.getpadypos() - padheight, w * 1.25, padheight)
            pygame.draw.rect(variables.screen, padcolor, padrect)
            variables.dirtyrects.append(padrect)

            # draw little pads if space pressed
            if self.spacepressedp:
                spacing = w*0.05
                padrect = Rect(padxspace * (x) - w / 8 + xoffset + spacing/2, variables.getpadypos() - padheight+spacing/2, w * 1.25-spacing, padheight-spacing)
                pygame.draw.rect(variables.screen, variables.notes_colors[x - 1], padrect)
                variables.dirtyrects.append(padrect)
            

        # draw the feedback (keys then scores, perfect ect)
        for x in range(0, 8):
            xoffset = 0
            if (x > 3):
                xoffset = middleoffset
            blitp = False
            if self.feedback_timers[x] != None:
                if variables.settings.current_time < self.feedback_timers[x]:
                    blitp = True
            else:
                blitp = True

            if blitp:
                bx = padxspace * (x + 1) - w / 8 + xoffset
                by = variables.getpadypos() - padheight
                bpic = self.getfeedbackpic(x)
                brect = Rect(bx, by, bpic.get_width(), bpic.get_height())
                variables.screen.blit(self.getfeedbackpic(x), (bx, by))
                variables.dirtyrects.append(brect)

    # returns number of notes that should have passed the pad by now
    def notetime(self):
        dt = variables.settings.current_time - self.starttime
        if (self.pausetime):
            dt -= variables.settings.current_time - self.pausetime
        notetime = (dt/self.tempo) - variables.settings.notes_per_screen
        return notetime

    # returns the pos of the bottom of the note
    def notepos(self, note):
        notetime = self.notetime()
        ypos = (notetime - note.time) * (variables.getpadypos() / variables.settings.notes_per_screen) + variables.getpadypos()
        if (note.screenvalue() > 3):
            xpos = note.screenvalue() * padxspace + middleoffset + padxspace
        else:
            xpos = note.screenvalue() * padxspace + padxspace
        return [xpos, ypos]

    def pos_to_score(self, ypos):
        difference = abs(ypos - variables.getpadypos())
        if difference <= variables.getperfectrange():
            return variables.perfect_value
        elif difference <= variables.getgoodrange():
            return variables.good_value
        elif difference <= variables.getokrange():
            return variables.ok_value
        elif difference <= variables.getmissrange():
            return variables.miss_value
        else:
            return None

    def get_note_place_from_value_begin(self, v):
        np = None
        notevalue = v
        for x in range(0, len(self.notes)):
            if self.notes[x].screenvalue() == v and self.notes[x].ison and self.notes[x].beginning_score == None:
                np = x
                notevalue = self.notes[x].value
                break
        return [np, notevalue]

    def get_note_place_from_value_end(self, v):
        np = None
        for x in range(0, len(self.notes)):
            if self.notes[x].screenvalue() == v and self.notes[x].ison and self.notes[x].end_score == None:
                np = x
                break
        return np

    def onkey(self, key):
        def check_note(np):
            if self.notes[np].beginning_score == None:
                s = self.pos_to_score(self.notes[np].pos[1] - padheight)

                
                if s != None:
                    # check if modifier is correct
                    if not self.notes[np].accidentalp == self.spacepressedp:
                        s = variables.miss_value
                    self.notes[np].beginning_score = s
                    if s == variables.miss_value:
                        self.notes[np].ison = False
                        self.feedback[self.notes[np].screenvalue()] = "miss"
                        self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo

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
            if self.spacepressedp:
                v += 1
            self.held_keys[kp] = v
            self.time_key_started[kp] = variables.settings.current_time
            play_tone(v)

        if variables.checkkey("note1", key):
            playnotepressed(0)
        elif variables.checkkey("note2", key):
            playnotepressed(1)
        elif variables.checkkey("note3", key):
            playnotepressed(2)
        elif variables.checkkey("note4", key):
            playnotepressed(3)
        elif variables.checkkey("note5", key):
            playnotepressed(4)
        elif variables.checkkey("note6", key):
            playnotepressed(5)
        elif variables.checkkey("note7", key):
            playnotepressed(6)
        elif variables.checkkey("note8", key):
            playnotepressed(7)
        elif variables.checkkey("notemodifier", key):
            self.spacepressedp = True

    def onrelease(self, key):

        def check_note(np):
            if self.notes[np].end_score == None and self.notes[np].beginning_score != None:
                top_of_note = self.notes[np].pos[1] - self.notes[np].height(self.tempo)
                s = self.pos_to_score(top_of_note)

                if s == None and self.notes[np].beginning_score != None:
                    s = variables.miss_value
                    self.notes[np].height_offset = self.notes[np].pos[1] - variables.getpadypos()

                if s != None:
                    
                    if s < self.notes[np].beginning_score:
                        final_note_score = s
                    else:
                        final_note_score = self.notes[np].beginning_score

                    self.notes[np].end_score = s

                    if s == variables.miss_value:
                        self.notes[np].height_offset = self.notes[np].pos[1] - variables.getpadypos()
                        self.notes[np].ison = False

                    self.scores.append(final_note_score)

                    if final_note_score == variables.miss_value:
                        self.feedback[self.notes[np].screenvalue()] = "miss"
                        self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.good_value:
                        self.feedback[self.notes[np].screenvalue()] = "good"
                        self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.ok_value:
                        self.feedback[self.notes[np].screenvalue()] = "ok"
                        self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo
                    elif final_note_score == variables.perfect_value:
                        self.feedback[self.notes[np].screenvalue()] = "perfect"
                        self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo
            # released before a note, penalty for randomly playing notes not written
            else:
                self.scores.append(variables.miss_value)
                self.feedback[self.notes[np].screenvalue()] = "miss"
                self.feedback_timers[self.notes[np].screenvalue()] = variables.settings.current_time + self.tempo

        def check_place(v):
            np = self.get_note_place_from_value_end(v)
            if not np == None:
                check_note(np)
            else:
                self.scores.append(variables.miss_value)
                self.feedback[v] = "miss"
                self.feedback_timers[v] = variables.settings.current_time + self.tempo

        if variables.checkkey("note1", key):
            check_place(0)
            stop_tone(self.held_keys[0])
            self.held_keys[0] = None
        elif variables.checkkey("note2", key):
            check_place(1)
            stop_tone(self.held_keys[1])
            self.held_keys[1] = None
        elif variables.checkkey("note3", key):
            check_place(2)
            stop_tone(self.held_keys[2])
            self.held_keys[2] = None
        elif variables.checkkey("note4", key):
            check_place(3)
            stop_tone(self.held_keys[3])
            self.held_keys[3] = None
        elif variables.checkkey("note5", key):
            check_place(4)
            stop_tone(self.held_keys[4])
            self.held_keys[4] = None
        elif variables.checkkey("note6", key):
            check_place(5)
            stop_tone(self.held_keys[5])
            self.held_keys[5] = None
        elif variables.checkkey("note7", key):
            check_place(6)
            stop_tone(self.held_keys[6])
            self.held_keys[6] = None
        elif variables.checkkey("note8", key):
            check_place(7)
            stop_tone(self.held_keys[7])
            self.held_keys[7] = None
        elif variables.checkkey("notemodifier", key):
            self.spacepressedp = False

    def ontick(self):
        # update positions of notes
        for n in self.notes:
            n.pos = self.notepos(n)
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
            smaller = min(h / 2, variables.getmissrange())

            if self.notes[x].pos[1] - smaller > variables.getpadypos() and self.notes[x].beginning_score == None:
                if self.notes[x].ison:
                    self.feedback[self.notes[x].screenvalue()] = "miss"
                    self.feedback_timers[self.notes[x].screenvalue()] = variables.settings.current_time + self.tempo
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

        # handle the drum machine
        # now dt is based on starttime
        notetime = self.notetime() + variables.settings.notes_per_screen
        # play a drum sound if it is on the beat, drumcounter increases 4 times per beat
        if (notetime*4 >= self.drumcounter+1):
            self.drumcounter += 1
            if self.drumcounter % 4 == 0:
                play_effect("onedrum")

    def reset_buttons(self):
        for x in range(8):
            self.held_keys[x] = None
        # turn off sound
        for x in range(-24, 24):
            stop_tone(x)
