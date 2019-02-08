import copy
from pygame import Rect

import graphics, pygame, variables
from graphics import getpicbywidth
from play_sound import stop_tone, play_tone, update_tone, play_effect

from Note import dancenamemap, dancenamemapdark


padheight = variables.height / 80

class Beatmap():

    def __init__(self, tempo, notes, specs):
        self.enemyspecs = specs
        
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
        # like held keys but for the modified versions of the key (accidentals)
        self.modifierheldkeys = [None] * 8
        # spaceheldq stores if the modifier key (default space) is currently being held
        self.spacepressedp = False
        # when to stop displaying the text, in milliseconds
        self.feedback_timers = [None] * 8
        self.feedbackcolor = [None] * 8
        self.feedback = []
        self.setfeedbacktocontrols(False)

        self.currentcombo = 0;
        self.roundmaxcombo = 0;
        self.timeoflastcomboaddition = 0;

        self.drumcounter = 0

        
    def setfeedbacktocontrols(self, modifiedp):
        self.feedback = []
        for x in range(8):
            if modifiedp:
                n = pygame.key.name(variables.settings.keydict["note" + str(x+1) + "modified"][0])
                self.feedbackcolor[x] = variables.PINK
            else:
                n = pygame.key.name(variables.settings.keydict["note" + str(x+1)][0])
                self.feedbackcolor[x] = variables.WHITE
            self.feedback.append(n)

    def pause(self):
        self.pausetime = variables.settings.current_time

    def unpause(self):
        self.starttime += variables.settings.current_time - self.pausetime
        self.pausetime = 0

    def showkeys(self, modifiedp = False):
        self.feedback_timers = [None] * 8
        self.setfeedbacktocontrols(modifiedp)


    def reset(self, battlestarttime, beginningq):
        self.scores = []
        self.roundmaxcombo = 0
        self.currentcombo = 0
        synctime = self.tempo - ((variables.settings.current_time - battlestarttime) % self.tempo)
        self.starttime = variables.settings.current_time + synctime
        self.showkeys()
        if not beginningq:
            self.notes = copy.deepcopy(self.originalnotes)
        self.drumcounter = 0

    def appendscore(self, score, noteplayed):
        for x in range(noteplayed.scoremultiplier):
            self.scores.append(score)
        if score == variables.miss_value:
            self.currentcombo = 0
        else:
            self.currentcombo += 1
            self.timeoflastcomboaddition = variables.settings.current_time
            if self.currentcombo>self.roundmaxcombo:
                self.roundmaxcombo = self.currentcombo
        
    def draw(self):

        self.draw_pads()
                    
        # draw the notes that are on the screen
        i = 0
        while i < len(self.notes):
            self.notes[i].draw(self.tempo)
            if self.notes[i].pos[1] < 0:
                break
            i += 1
        
        

        # also draw notetime to top left
        if variables.devmode:
            notetimetext = variables.font.render(str(self.notetime()), 0, variables.WHITE)
            variables.screen.blit(notetimetext, [10, 2*variables.font.get_linesize()])

    def getfeedbackpic(self, index):
        color = variables.WHITE
        if self.feedbackcolor[index] != None:
            color = self.feedbackcolor[index]
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
        pic = graphics.getTextPic(s, variables.gettextsize(), color)
        if rotatep:
            pic = pygame.transform.rotate(pic, -45)
        return pic

    def draw_one_presspad(self, index):
        
        # draw which ones are pressed
        if not variables.settings.dancepadmodep:
            w = variables.notewidth()
            ew = w * 1.25
            padellipseypos = variables.getpadypos() - padheight + padheight / 2 - ew / 4
            padcolor = (180, 180, 180)
            if self.modifierheldkeys[index] != None:
                padcolor = (variables.PINK[0]-70, variables.PINK[1]-30, variables.PINK[2]-70)
            elif self.spacepressedp:
                padcolor = (variables.PINK[0]-70, variables.PINK[1]-30, variables.PINK[2]-70)

            if self.held_keys[index] != None or self.modifierheldkeys[index] != None:
                expos = Beatmap.screenvaltoxpos(index) - w / 8
                pygame.draw.ellipse(variables.screen, padcolor, [expos,
                                                                        padellipseypos,
                                                                        ew, ew / 2])
                variables.dirtyrects.append(Rect(expos, padellipseypos, ew, ew/2))

    def draw_one_pad(self, index):
        w = variables.notewidth()
        padcolor = variables.notes_colors[index]
        if(self.spacepressedp):
            padcolor = variables.PINK

        # draw the pads
        if variables.settings.dancepadmodep:
            padrect = Rect(Beatmap.screenvaltoxpos(index), variables.getpadypos()-variables.dancearrowwidth(), variables.dancearrowwidth(), variables.dancearrowwidth())
            arrowpic = None
            if self.held_keys[index] != None or self.modifierheldkeys[index] != None:
                arrowpic = dancenamemap[index]
            else:
                arrowpic = dancenamemapdark[index]

            variables.screen.blit(getpicbywidth(arrowpic, variables.dancearrowwidth()), padrect)
            variables.dirtyrects.append(padrect)
        else:
            padrect = Rect(Beatmap.screenvaltoxpos(index)- w / 8, variables.getpadypos() - padheight, w * 1.25, padheight)
            pygame.draw.rect(variables.screen, padcolor, padrect)
            variables.dirtyrects.append(padrect)

        # draw little pads if space pressed
        if self.spacepressedp and not variables.settings.dancepadmodep:
            spacing = w*0.05
            padrect = Rect(Beatmap.screenvaltoxpos(index) - w / 8+ spacing/2, variables.getpadypos() - padheight+spacing/2, w * 1.25-spacing, padheight-spacing)
            pygame.draw.rect(variables.screen, variables.notes_colors[index], padrect)
            variables.dirtyrects.append(padrect)

                
    def draw_pads(self):
        numbertodraw = 8
        if variables.settings.dancepadmodep:
            numbertodraw = 4


        # draw bottom rectangles
        for x in range(numbertodraw):
            self.draw_one_presspad(x)

            self.draw_one_pad(x)
            

        # draw the feedback (keys then scores, perfect ect)
        for x in range(0, 8):
            blitp = False
            if self.feedback_timers[x] != None:
                if variables.settings.current_time < self.feedback_timers[x]:
                    blitp = True
            else:
                blitp = True

            if blitp:
                bx = Beatmap.screenvaltoxpos(x) - variables.notewidth() / 8 
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

    @staticmethod
    def screenvaltoxpos(screenval):
        
        padxspace = variables.width / 12
        middleoffset = padxspace / 2

        xpos = 0
        if (screenval > 3):
            xpos = screenval * padxspace + middleoffset + padxspace
        else:
            xpos = screenval * padxspace + padxspace
        return xpos


    # returns the pos of the bottom of the note
    def notepos(self, note):
        notetime = self.notetime()
        ypos = (notetime - note.time) * (variables.getpadypos() / variables.settings.notes_per_screen) + variables.getpadypos()
        return [Beatmap.screenvaltoxpos(note.getscreenvalue()), ypos]

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
            if self.notes[x].getscreenvalue() == v and self.notes[x].ison and self.notes[x].beginning_score == None:
                np = x
                notevalue = self.notes[x].value
                break
        return [np, notevalue]

    def get_note_place_from_value_end(self, v):
        np = None
        for x in range(0, len(self.notes)):
            if self.notes[x].getscreenvalue() == v and self.notes[x].ison and self.notes[x].end_score == None:
                np = x
                break
        return np

    def setfeedback(self, index, string):
        self.feedback[index] = string
        self.feedback_timers[index] = variables.settings.current_time + self.tempo
        self.feedbackcolor[index] = variables.WHITE

    def process_final_score(self, note, endscore):
        final_note_score = None
        if endscore < note.beginning_score:
            final_note_score = s
        else:
            final_note_score = note.beginning_score

        note.end_score = endscore

        
        note.ison = False
        # if it was missed in the later half, set the height offset for drawing
        if note.beginning_score != variables.miss_value and endscore == variables.miss_value:
            note.height_offset = note.pos[1] - variables.getpadypos()

        self.appendscore(final_note_score, note)

        if final_note_score == variables.miss_value:
            self.setfeedback(note.getscreenvalue(), "miss")
        elif final_note_score == variables.good_value:
            self.setfeedback(note.getscreenvalue(), "good")
        elif final_note_score == variables.ok_value:
            self.setfeedback(note.getscreenvalue(), "ok")
        elif final_note_score == variables.perfect_value:
            self.setfeedback(note.getscreenvalue(), "perfect")
    
    def onkey(self, key):
        def check_note(np, modifiedp):
            if self.notes[np].beginning_score == None:
                s = self.pos_to_score(self.notes[np].pos[1] - padheight)
                
                if s != None:
                    # check if modifier is correct
                    if not self.notes[np].accidentalp == modifiedp:
                        s = variables.miss_value

                    
                    self.notes[np].beginning_score = s

                    # just process right away if dancepadmode
                    if variables.settings.dancepadmodep:
                        self.process_final_score(self.notes[np], s)
                    # also if it missed, process right away
                    elif s == variables.miss_value:
                        self.process_final_score(self.notes[np], s)
                    

        # returns the value for the sound produced
        def check_place(v, modifiedp):
            placeandvalue = self.get_note_place_from_value_begin(v)
            np = placeandvalue[0]
            if not np == None:
                check_note(np, modifiedp)
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

        def playnotepressed(kp, modifiedp):
            v = check_place(kp, modifiedp)
            v = simple_value_in_key(v)
            if self.spacepressedp or modifiedp:
                v += 1
            play_tone(v, self.enemyspecs["volumeenvelope"], self.numofupdatetones)
            self.numofupdatetones += 1
            if modifiedp:
                self.modifierheldkeys[kp] = v
            else:
                self.held_keys[kp] = v

        for x in range(8):
            if variables.checkkey("note" + str(x+1), key):
                playnotepressed(x, self.spacepressedp)
                break
        
        if variables.checkkey("notemodifier", key):
            self.spacepressedp = True

        for x in range(8):
            if variables.checkkey("note" + str(x+1) + "modified", key):
                playnotepressed(x, True)

    def onrelease(self, key):

        def check_note(np):
            if self.notes[np].end_score == None and self.notes[np].beginning_score != None:
                top_of_note = self.notes[np].pos[1] - self.notes[np].height(self.tempo)
                s = self.pos_to_score(top_of_note)

                if s == None and self.notes[np].beginning_score != None:
                    s = variables.miss_value
                    self.notes[np].height_offset = self.notes[np].pos[1] - variables.getpadypos()

                if s != None:
                    self.process_final_score(self.notes[np], s)
                    
            # potential hard mode: released before a note a miss

            
        def check_place(v):
            np = self.get_note_place_from_value_end(v)
            if not np == None:
                check_note(np)

            # potential hard mode: make a press without a note a miss

        for x in range(8):
            if variables.checkkey("note" + str(x+1), key):
                # do the same for both modified and unmodified keys for check place, only start matters
                check_place(x)
                if self.held_keys[x] != None:
                    stop_tone(self.held_keys[x])
                self.held_keys[x] = None
                break
            elif variables.checkkey("note" + str(x+1) + "modified", key):
                check_place(x)
                if self.modifierheldkeys[x] != None:
                    stop_tone(self.modifierheldkeys[x])
                self.modifierheldkeys[x] = None
                break

        if variables.checkkey("notemodifier", key):
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
                    self.notes[x].beginning_score = variables.miss_value
                    self.process_final_score(self.notes[x], variables.miss_value)
                elif self.notes[x].pos[1] < 0:
                    # if you are in a part of the list before the screen, don't keep checking
                    # (assuming the list of notes must be ordered by time, of course)
                    break

        
        # update played notes for looping
        for k in self.held_keys:
            if not k == None:
                update_tone(k, self.enemyspecs["volumeenvelope"], self.numofupdatetones)
                self.numofupdatetones += 1

         # update played notes for looping
        for k in self.modifierheldkeys:
            if not k == None:
                update_tone(k, self.enemyspecs["volumeenvelope"], self.numofupdatetones)
                self.numofupdatetones += 1

        # handle the drum machine
        # now dt is based on starttime
        notetime = self.notetime() + variables.settings.notes_per_screen
        # play a drum sound if it is on the beat, drumcounter increases 4 times per beat
        if (notetime*4 >= self.drumcounter+1):
            self.drumcounter += 1

        # reset numofupdatetones for next frame
        self.numofupdatetones = 0
            
    def reset_buttons(self):
        for x in range(8):
            self.held_keys[x] = None
        for x in range(8):
            self.modifierheldkeys[x] = None
        # turn off sound
        for x in range(-24, 24):
            stop_tone(x)
