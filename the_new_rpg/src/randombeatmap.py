from Beatmap import Beatmap
from Note import  Note
from random import randint

#level is the level of the enemy
def very_random(lv):
    beatmaps = []
    maxtime = 15+lv
    for x in range(5):
        beatmaps.append(very_random_beatmap(lv, randint(maxtime, maxtime+lv)))
    return beatmaps

def very_random_beatmap(lv, maxtime):
    #makes sure the new one is not the same as the old one
    def random_value(previous):
        r = randint(1, 8)
        if r == previous:
            return random_value(previous)
        else:
            return r

    l = []
    time = 1
    while time < maxtime:
        if time>(maxtime-2):
            duration = maxtime-time
            #make the last note the tonic
            if (l[-1].value == 1):
                l.append(Note(8, time, duration))
            else:
                l.append(Note(1, time, duration))
        else:
            duration = 1
            if(randint(0,50)<(lv+2)**2):
                if(randint(1, 2) == 1):
                    duration = 2
                if(randint(0,500)<(lv+2)**2):
                    if(randint(1, 2) == 1):
                        if(randint(1, 3) == 1):
                            duration = 3
                        else:
                            duration = 4
            #so that usually it is the inverse, short notes
            if(randint(1, 3)>1):
                duration = 1/duration

            #if it is on an offbeat
            if(time%1 == 0.5):
                if(randint(0, 100)>lv**2):
                    if(randint(1, 2) == 1):
                        duration = 0.5
            elif((time%1)>0):
                #want to fix offbeats less that 0.5 quickly
                if(randint(0, 1000)>lv**2):
                    duration = 1-(time%1)

            if len(l) > 0:
                l.append(Note(random_value(l[-1].value), time, duration))
            else:
                l.append(Note(randint(1, 8), time, duration))
        time += duration
    tempo = (1200*3)/(lv+3)
    return Beatmap(tempo, l)

#like very random but beatmaps after the first one are based off of the first one
def very_random_v(lv):
    beatmaps = []
    maxtime = 15+lv
    beatmaps.append(very_random_beatmap(lv, randint(maxtime, maxtime+lv)))
    for x in range(4):
        beatmaps.append(very_random_variation(beatmaps[-1]))
    return beatmaps

def very_random_variation(last_beatmap):
    #makes sure the new one is not the same as the old one
    def random_value(previous):
        r = randint(1, 8)
        if r == previous:
            return random_value(previous)
        else:
            return r

    l = []
    x = 0
    while x < len(last_beatmap.notes):
        oldnote = last_beatmap.notes[x]
        #sometimes change the value of the note
        if(randint(1, 5) == 1 and x != len(last_beatmap.notes)-1):
            if len(l) > 0:
                l.append(Note(random_value(l[-1].value), oldnote.time, oldnote.duration))
            else:
                l.append(Note(randint(1, 8), oldnote.time, oldnote.duration))
        else:
            l.append(Note(oldnote.value, oldnote.time, oldnote.duration))
        x+=1
    return Beatmap(last_beatmap.tempo, l)