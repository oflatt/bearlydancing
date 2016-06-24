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
            #make the last note the tonic
            if (l[-1].value == 1):
                l.append(Note(8, time, maxtime-time))
            else:
                l.append(Note(1, time, maxtime-time))
        else:
            if len(l) > 0:
                l.append(Note(random_value(l[-1].value), time, 1))
            else:
                l.append(Note(randint(1, 8), time, 1))
        time += 1
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
        #sometimes change the value of the note
        if(randint(1, 3) == 1):
            if len(l) > 0:
                l.append(Note(random_value(l[-1].value), last_beatmap.notes[x].time, 1))
            else:
                l.append(Note(randint(1, 8), last_beatmap.notes[x].time, 1))
        else:
            l.append(last_beatmap.notes[x])
        x+=1
    return Beatmap(last_beatmap.tempo, l)