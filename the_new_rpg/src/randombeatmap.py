from Beatmap import Beatmap
from Note import  Note
from Note import value_to_screenvalue
import random
from random import randint
import variables

testmapa = Beatmap((1200*3)/4, [Note(-7, 2, 2), Note(-6, 1, 1)])
testmapb = [Beatmap((1200*3)/4, [Note(0, 1, 1), Note(0, 4, 1), Note(0, 5, 1), Note(1, 6, 1)])]
testmap = [Beatmap((1200*3)/4, [Note(0, 1, 0.9), Note(-1, 2, 1), Note(8, 3, 1), Note(14, 5, 1), Note(-7, 6, 1)])]

def myrand(n):
    if(randint(0, n) > (n-1)):
        return False
    else:
        return True

def shorten_doubles(l):
    newl = l
    x = 0
    while (x < len(l)):
        y = 1
        while x+y<len(l):
            if l[x+y].time <= l[x].time+l[x].duration:
                if l[x].screenvalue == l[x+y].screenvalue:
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
        duration = rand_duration(time, lv)
        rv = random_value(time, ischord, l, specs)
        # if it is not a rest
        if (not rv == "rest"):
            if (ischord):
                l.insert(len(l) - 1, Note(rv, time, duration))
            else:
                l.append(Note(rv, time, duration))
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
    #choose a random value, with rules
    rv = randint(variables.minvalue, variables.maxvalue)

    #handeling rests, 8/9 times it will be a note
    if("melodic" in specs):
        if(not(myrand(8))):
            rv = "rest"

    def melodicchord(rv):
        value = rv
        lastv = l[-1].value

        #3/4 are within 6
        if(myrand(3)):
            rd = randint(1, 6)
            if (myrand(1)):
                rd = -rd
            value = lastv + rd

        # if it is outside the range
        if (value < variables.minvalue or value > variables.maxvalue):
            return melodicchord(rv)
        else:
            return value

    def melodic(rv):
        value = rv
        lastv = l[-1].value

        #2/3 chance of being 1 or 2 away from previous note
        if (myrand(2)):
            # half chance of continuing same direction
            if (len(l) > 1):
                if ((lastv - 1 == l[-2].value or lastv + 1 == l[-2].value) and myrand(1)):
                    value = lastv + (lastv - l[-2].value)
            else:
                #near previous note
                rd = randint(1, 2)
                if(myrand(1)):
                    rd = -rd
                value = lastv + rd
        #within 6
        elif(myrand(1)):
            rd = randint(1, 6)
            if (myrand(1)):
                rd = -rd
            value = lastv + rd
        #otherwise use the random value
        else:
            value = rv

        if (len(l) > 1):
            # if there was a jump previously
            if (lastv > l[-2].value + 2):
                # 2/3 chance to go back one note
                if (myrand(2)):
                    value = lastv-1
            elif(lastv < l[-2].value-2):
                if(myrand(2)):
                    value = lastv+1

        #if it is outside the range
        if(value < variables.minvalue or value>variables.maxvalue):
            return melodic(rv)
        else:
            return value


    if(('melodic' in specs['rules']) and not(ischord) and len(l)>0 and not rv == "rest"):
        rv = melodic(rv)
    elif(('melodic' in specs['rules']) and ischord and not rv == "rest"):
        rv = melodicchord(rv)


    iscopy = False
    if(not rv == "rest"):
        #make sure the value does not overlap another one
        x = 0
        while (x < len(l)):
            if (l[x].time + l[x].duration > t and l[x].screenvalue == value_to_screenvalue(rv)):
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

    #additional chance at lower levels to be slow
    if(randint(0, 5)>lv):
        d = 2

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
