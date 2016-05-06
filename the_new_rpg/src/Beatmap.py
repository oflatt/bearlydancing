import variables

padypos = variables.height*(3/4)
padxspace = variables.width/10

class Beatmap():
    scale = [50, 53, 55, 58, 60, 64, 68, 70] #list of eight pitches
    speed = 1
    starttime = 0

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
            n[x].draw(self.notepos(n[x]))

    def notes_on_screen(self):
        n = []
        for x in range(0, len(self.notes)):
            checkednote = self.notes[x]
            if self.notepos(checkednote)[1] > 0:
                n.insert(0, checkednote)
            else:
                break
        return n

    def notepos(self, note):
        dt = variables.current_time-self.starttime
        #ypos finds the notes place relative to pads then offsets it
        ypos = (dt-(note.time*self.tempo))*variables.dancespeed*0.1 + padypos
        xpos = note.value*padxspace
        print(ypos)
        return [xpos, ypos]