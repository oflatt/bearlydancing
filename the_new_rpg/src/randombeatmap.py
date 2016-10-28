from Beatmap import Beatmap
from Note import  Note
from random import randint
import variables, random

testmapb = [Beatmap((1200*3)/4, [Note(0, 1, 1), Note(0, 4, 1), Note(0, 5, 1), Note(1, 6, 1)])]
testmap = [Beatmap((1200*3)/4, [Note(0, 1, 0.9), Note(-1, 2, 1), Note(8, 3, 1), Note(14, 5, 1), Note(-7, 6, 1)])]

def shorten_doubles(l):
    newl = l
    x = 0
    while (x < len(l)):
        y = 1
        while x+y<len(l)-1:
            if l[x+y].time <= l[x].time+l[x].duration:
                if l[x].value == l[x+y].value:
                    newl[x].duration -= 0.1
                    break
            else:
                break
            y += 1
        x += 1
    return newl

def random_beatmap(specs):
    l = []
    lv = specs["lv"]
    maxtime = specs["maxtime"]

    def addnote(time, ischord):
        # last note
        if time > (maxtime - 2):
            duration = maxtime - time
            # if it is the third or fifth in the chord
            if (ischord):
                if (randint(1, 2) == 1):
                    l.append(Note(3, time, duration))
                else:
                    l.append(Note(5, time, duration))
            else:
                # make the last note the tonic
                if (l[-1].value == 1):
                    l.append(Note(8, time, duration))
                else:
                    l.append(Note(1, time, duration))
        # normal notes
        else:
            duration = rand_duration(time, lv)
            # if it is not a rest
            if (randint(1, 9) != 1):
                if (ischord):
                    l.insert(len(l) - 1, Note(random_value(time, ischord, l, specs), time, duration))
                else:
                    l.append(Note(random_value(time, ischord, l, specs), time, duration))
        return duration

    time = 1
    while time < maxtime:
        oldt = time
        time += addnote(oldt, False)
        # chance to add more notes at the same time
        if (randint(0, 100) < (lv + 2) ** 2):
            if (randint(1, 2) == 1):
                addnote(oldt, True)
            if (randint(0, 1000) < (lv + 2) ** 2):
                addnote(oldt, True)

    tempo = (1200 * 3) / ((lv / 3) + 3.5)
    l = shorten_doubles(l)
    return Beatmap(tempo, l)


def random_value(t, ischord, l, specs):
    #choose a random value
    rv = randint(-variables.maxvalue, variables.maxvalue)

    #old code for continuing same direciton
    # if ((not ischord)):
    #     if (len(l) > 1):
    #         lastv = l[-1].value
    #         # if we continue in the same direction
    #         if ((lastv - 1 == l[-2].value or lastv + 1 == l[-2].value) and random.choice([True, False])):
    #             rv = lastv + (lastv - l[-2].value)
    #         else:
    #             if (random.choice([True, False, False])):
    #                 rv = lastv + random.choice([-1, 1])
    #             elif (random.choice([True, False, False])):
    #                 rv = lastv + random.choice([-2, 2])
    #             else:
    #                 rv = randint(1, 8)
    #     else:
    #         rv = randint(0, 48)
    # else:
    #     rv = randint(0, 48)

    #make sure the value does not overlap another one
    iscopy = False
    x = 0
    while (x < len(l)):
        if (ischord):
            if (l[x].time + l[x].duration > t): #and (l[x].value == rv or l[x].value + 1 == rv or l[x].value - 1 == rv)): this is to avoid ugly chords
                iscopy = True
                break
        else:
            if (l[x].time + l[x].duration > t and l[x].value == rv):
                iscopy = True
                break
        x += 1

    if (iscopy):
        #try again if it is a copy
        return random_value(t, ischord, l, specs)
    else:
        return rv


def rand_duration(time, lv):
    d = 1
    if (randint(0, 50) < (lv + 2) ** 2):
        if (randint(1, 2) == 1):
            d = 2
        if (randint(0, 500) < (lv + 2) ** 2):
            if (randint(1, 2) == 1):
                if (randint(1, 3) == 1):
                    d = 3
                else:
                    d = 4
    # so that usually it is the inverse, short notes
    if (randint(1, 3) > 1):
        d = 1 / d

    # if it is on an offbeat
    if (time % 1 == 0.5):
        if (randint(0, 100) > lv ** 2):
            if (randint(1, 2) == 1):
                d = 0.5
    elif ((time % 1) > 0):
        # want to fix offbeats less that 0.5 quickly
        if (randint(0, 1000) > lv ** 2):
            d = 1 - (time % 1)
    return d