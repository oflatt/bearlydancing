# random_beatmap is the entrypoint- values and durations are calculated separetly
# the note list in the end should be ordered early notes first
# notes added on generatively- each "layer" has the main melody note at the back of the list, chord notes inserted before it

from Beatmap import Beatmap
from Note import Note
from Note import value_to_screenvalue
from Note import compare_around
import random, copy
from random import randint
import variables, math

''' rule types for beatmaps (in specs)
-------- for values -----------
melodic- higher chance of notes being in a row in one direction
skippy- high chance of note value being 2 away, with continuing direction chance, only melodic
alternating- high chance to go back to a note or be near the previous note, and if not further away, uses melodic chords
rests- high chance of shorter notes and rests in between notes

------- repeat ----------------
repeat- repeats sections with variations
repeatmove- repeats sections with all the tones shifted
repeatmovevariation- like repeatmove but calls the variation function on repeated sectons as well (combines repeat and repeatmove)
repeatbig- not implemented yet, would be an aditional layer of repetition for a large phrase with variation

------ repeat separated -------
repeatrhythm- like repeat, but uses only the times and durations for the last few notes
repeatvalues- like repeat, but uses only the values and computes new durations for the values

cheapending- pick a random tonic and throw it on the end
'''


def printnotelist(l):
    for x in l:
        isc = ""
        if x.chordadditionp:
            isc = " +chordaddition"
        print("value: " + str(x.value) + " time: " + str(x.time) + " duration: " + str(x.duration) + isc)


testmapa = [Beatmap((1200 * 3) / 4, [Note(-7, 2, 2), Note(-6, 1, 1)])]
testmapb = [Beatmap((1200 * 3) / 4, [Note(0, 1, 1), Note(0, 4, 1), Note(0, 5, 1), Note(1, 6, 1)])]
testmap = [Beatmap((1200 * 3) / 4, [Note(0, 1, 0.2), Note(0, 1.3, 0.1), Note(0, 2, 0.4), Note(0, 2.5, 0.4), Note(0, 3, 0.4),
                                    Note(0, 3.5, 0.4), Note(0, 4, 0.4), Note(0, 4.5, 0.4), Note(0, 5, 0.4), Note(0, 5.5, 0.4),
                                    Note(0, 6, 0.4), Note(0, 6.5, 0.4), Note(0, 7, 0.4), Note(0, 7.5, 0.4), Note(0, 8, 0.4)])]


# if n is 2, then there is a 2/3 chance of true
def myrand(n):
    if (randint(0, n) < n):
        return True
    else:
        return False


# q stands for question mark
def outsiderangeq(value):
    return value < variables.minvalue or value > variables.maxvalue

# checks if a a note collides with a list of notes
def notecollidep(ntime, nvalue, nduration, l):
    iscopy = False
    x = 0
    while (x < len(l)):
        if l[x].screenvalue() == value_to_screenvalue(nvalue):
            if l[x].time+l[x].duration > ntime and l[x].time < ntime+nduration:
                iscopy = True
                break
        x += 1
    return iscopy

# checks if the notes are in proper order by time (time increasing)
def notetimeorderedp(l):
    maxt = 0
    orderedp = True
    for n in l:
        if n.time < maxt:
            orderedp = False
            break
        elif n.time > maxt:
            maxt = n.time
    return orderedp

# checks to make sure that chord notes are behind the melody notes
def notechordorderedp(l):
    orderedp = True
    # check all but last note
    for i in range(len(l)-1):
        n = l[i]
        if n.chordadditionp:
            if not n.time == l[i+1].time:
                orderedp = False
                break
    return orderedp

def thrownoteerror(errorstring):
    print("------------------------------")
    print("ERROR: " + errorstring)
    print("------------------------------")
    

def shorten_doubles(l):
    newl = l
    x = 0
    while (x < len(l)):
        y = 1
        while x + y < len(l):
            if l[x + y].time <= l[x].time + l[x].duration:
                if l[x].screenvalue() == l[x + y].screenvalue():
                    newl[x].duration -= 0.1
                    break
            else:
                break
            y += 1
        x += 1
    return newl


def movednotes(old_notes, movelength):
    l = copy.deepcopy(old_notes)

    # find the max and min values
    maxval = l[0].value
    minval = l[0].value
    for n in l:
        if n.value > maxval:
            maxval = n.value
        if n.value < minval:
            minval = n.value

    #print(str(maxval) + "  " + str(minval) + "  " + str(movelength))
    if outsiderangeq(maxval + 1) and outsiderangeq(minval - 1):
        return l
    elif outsiderangeq(maxval + movelength) or outsiderangeq(minval + movelength):
        return movednotes(l, randint(-4, 4))
    else:
        for n in l:
            n.newvalue(n.value + movelength)
        return l


# returns a dictionary with timetoadd and the list
# timetoadd is an extra offset that is used for recursive calls
# repeatlength is the number of notes to repeat
# movelength is an offset for values of notes
def repetition(timetoadd, movelength, listofnotes, repeatlength, specs, maxtimetaken):
    print("repetition: time to add: " + str(timetoadd) + " repeatlength: " + str(repeatlength) + " last note time: " + str(listofnotes[-1].time))
    l = listofnotes.copy()

    # add on the last repeatlength notes again, varied
    notestoadd = l[-repeatlength:len(l)]
    
    # with certain rules we want to call variation of notes on the list
    if "repeat" in specs["rules"] or "repeatmovevariation" in specs["rules"]:
        notestoadd = variation_of_notes(notestoadd)

    if "repeatmove" in specs["rules"] or "repeatmovevariation" in specs["rules"]:
        notestoadd = movednotes(notestoadd, movelength)

    oldendtime = notestoadd[-1].time + notestoadd[-1].duration
    
    # calculate when to start next note so that the first note is on the same part of the beat as it was
    newstarttime = oldendtime + abs(oldendtime%1 - notestoadd[0].time%1)
    offsetfactor = newstarttime- notestoadd[0].time

    # offset the notestoadd by the offsetfactor
    for n in notestoadd:
        n.time += offsetfactor

    timetakensofar = timetoadd+offsetfactor

    l.extend(notestoadd)

    # chance to repeat section moved again
    if "repeatmove" in specs["rules"] or "repeatmovevariation" in specs["rules"] and timetakensofar<maxtimetaken:
        # if we have already added an extra
        returnval = {"timetaken": timetakensofar, "list": l}
        if timetoadd > 0:
            if myrand(1):
                returnval = repetition(timetakensofar, movelength, l, repeatlength, specs, maxtimetaken)
        else:
            if myrand(2):
                returnval = repetition(timetakensofar, movelength, l, repeatlength, specs, maxtimetaken)
        return returnval
    else:
        return {"timetaken": timetakensofar, "list": l}

# def random_beatmap(specs):
#     return testmap[0]

# returns a tuple with a new list and the duration of the new note
def addnote(notelist, time, ischord, specs):
    lv = specs["lv"]
    l = notelist.copy()
    duration = random_duration(time, l, specs, False)
    # if it is a chord, chance that the duration is the same as the melody
    if ischord:
        if randint(0, 100) > ((lv/1.8) + 2) ** 2:
            duration = l[-1].duration

    rv = random_value(time, ischord, l, specs)
    # chord notes added before the main note to make it easier to compare to the melody
    if ischord:
        l.insert(len(l) - 1, Note(rv, time, duration, True))
    else:
        l.append(Note(rv, time, duration))

    return (l, duration)

# returns a new list and the duration of the layer in a tuple
def addlayer(notelist, time, specs):
    lv = specs["lv"]
    isr = restp(time, notelist, specs)

    if isr:
        return (notelist, random_duration(time, notelist, specs, True))
    else:
        oldt = time
        notedurations = []
        addn = addnote(notelist, oldt, False, specs)
        l = addn[0]
        notedurations.append(addn[1])

        # chance to add chord notes, if it is not a rest
        if (randint(0, 100) < ((lv/2) + 2) ** 2):
            if randint(1, 2) == 1:
                addn = addnote(l, oldt, True, specs)
                l = addn[0]
                notedurations.append(addn[1])
            if randint(0, 1000) < (lv + 2) ** 2:
                addn = addnote(l, oldt, True, specs)
                l = addn[0]
                notedurations.append(addn[1])

        return (l, max(notedurations))

def random_beatmap(specs):
    variation_of_notes([])
    l = []
    lv = specs["lv"]
    maxtime = specs["maxtime"]
    maxtime = maxtime + lv * 2
    time = 1
    # repeatlength used in repeat rule for how many notes back to copy
    repeatlength = randint(3, 7 + lv)

    
    # masterloop for adding on notes
    while time < maxtime:
        print(time)
        addlayerp = False
        if "repeat" in specs["rules"] or "repeatmove" in specs["rules"] or "repeatmovevariation" in specs["rules"]:
            # if we do a repetition
            if (randint(-1, len(l) % repeatlength) == 0 and len(l) >= repeatlength):
                # add on the last repeatlength notes again, varied
                r = repetition(0, randint(-4, 4), l, repeatlength, specs, maxtime-time)
                l = r["list"]
                time += r["timetaken"]
            else:
                addlayerp = True
        else:
            addlayerp = True
            
        if addlayerp:
            addl = addlayer(l, time, specs)
            l = addl[0]
            time += addl[1]

    if ("cheapending" in specs["rules"]):
        lastvalue = random.choice([variables.minvalue, variables.maxvalue, 0])
        startt = round(l[-1].time + l[-1].duration + 0.5)
        l.append(Note(lastvalue, startt, randint(1,2)))

    # tempo is milliseconds per beat
    tempo = (1200 * 3) / ((lv / 4.5) + 3.5)
    l = shorten_doubles(l)

    if variables.devmode:
        print("output of:")
        print(specs["rules"])
        printnotelist(l)

    # then perform checks
    if not notetimeorderedp(l):
        thrownoteerror("note list not ordered properly for time")
    if not notechordorderedp(l):
        thrownoteerror("note list not ordered properly for chords")
        
    return Beatmap(tempo, l)


# random last is to get a random not of the ones last added, so that we don't compare parts of a chord
# depth is how many layers of times for notes we remove
# l is a list of notes where the earlier ones have later times
def random_last(depth, l):
    # removed is how far in the list to go to get the note
    removed = 0
    # first remove layers to satify depth
    for namethatdoesnotmatter in range(depth):
        timeoflast = l[removed].time
        while (l[removed].time == timeoflast):
            if (removed >= len(l)):
                break
            else:
                removed += 1

    if (removed >= len(l)):
        raise NotImplementedError("List does not have enough layers of depth")

    possibles = []
    x = 0
    timeoflast = l[removed].time
    while (l[removed + x].time == timeoflast):
        possibles.append(l[removed + x])
        if (removed + x >= len(l) - 1):
            break
        else:
            x += 1
    return random.choice(possibles)


# testl = [Note(5, 1, 2), Note(6, 2, 1), Note(6, 4, 1), Note(2, 5, 2), Note(3, 6, 4)]
# print(random_last(0, testl).value)
# print(random_last(1, testl).value)

# returns how "deep" a list is, how many layers of time it has
def notedepth(l):
    d = 0
    x = 0
    if (len(l) == 0):
        return 0
    else:
        lasttime = l[0].time
        while (x < len(l)):
            if (l[x].time != lasttime):
                d += 1
                lasttime = l[x].time
            x += 1
        return d


# assume depth>0
def melodic_value(rv, depth, specs, l):
    value = rv
    lastv = random_last(0, l).value

    # have a big chance of 2 away if "skippy" rule is on
    if ('skippy' in specs["rules"]) and myrand(3):
        if depth > 1:
            secondv = random_last(1, l).value
            # chance to continue same direction
            if (abs(lastv - secondv) == 1 or abs(lastv - secondv) == 2) and myrand(2):
                if (lastv > secondv):
                    value = lastv + 2
                else:
                    value = lastv - 2
            else:
                if myrand(1):
                    value = lastv + 2
                else:
                    value = lastv - 2
        else:
            if myrand(1):
                value = lastv + 2
            else:
                value = lastv - 2

    # 2/3 chance of being 1 or 2 away from previous note
    elif (myrand(2)):
        # 2/3 chance of continuing same direction
        if (depth > 1):
            secondv = random_last(1, l).value
            if ((lastv - 1 == secondv or lastv + 1 == secondv) and myrand(2)):
                value = lastv + (lastv - secondv)
            else:
                # near previous note
                rd = randint(1, 2)
                if (myrand(1)):
                    rd = -rd
                value = lastv + rd
        else:
            # near previous note
            rd = randint(1, 2)
            if (myrand(1)):
                rd = -rd
            value = lastv + rd

    # within 6
    elif (myrand(1)):
        rd = randint(1, 6)
        if (myrand(1)):
            rd = -rd
        value = lastv + rd
    # otherwise use the random value
    else:
        value = rv

    if (depth > 1):
        secondv = random_last(1, l).value
        # if there was a jump previously
        if (lastv > secondv + 2):
            # 2/3 chance to go back one note
            if (myrand(2)):
                value = lastv - 1
        elif (lastv < secondv - 2):
            if (myrand(2)):
                value = lastv + 1

    # if it is outside the range
    if (outsiderangeq(value)):
        return melodic_value(rv, depth, specs, l)
    else:
        return value


def alternating_value(rv, depth, specs, l):
    value = rv
    lastv = random_last(0, l).value

    def not_alternating():
        #print("non")
        distance_away = 0
        if myrand(1):
            distance_away = randint(3, 5)
        elif myrand(1):
            distance_away = randint(4, 6)
        elif myrand(1):
         #   print('far')
            distance_away = randint(1, 7)

        if myrand(1):
            distance_away = -distance_away

        if (distance_away != 0):
            if outsiderangeq(rv + distance_away):
                return not_alternating()
            else:
                return rv + distance_away
        else:
            return rv

    if depth > 1:
        secondv = random_last(1, l).value
        # if we actually do a alternation
        if myrand(4) and lastv != secondv:
            # half chance to pick same secondv note
            if myrand(1):
                value = secondv
            # otherwise pick a note close to it
            else:
                # within one
                if myrand(3):
                    value = secondv + random.choice([1, -1])
                # otherwise within 2
                else:
                    value = secondv + random.choice([1, 2, -1, -2])
        else:
            value = not_alternating()
    else:
        value = not_alternating()

    if outsiderangeq(value):
        return alternating_value(rv, depth, specs, l)
    else:
        return value

def restp(t, l, specs):
    isr = False
    # handeling rests
    if (len(l) > 0):
        if ("rests" in specs["rules"] and l[-1].time + l[-1].duration >= t):
            # high chance of a rest if the last note was not a rest
            if (myrand(4)):
                isr = True
    # 8/9 a rest if not rests rule
        elif not myrand(8):
            isr = True

    return isr

def random_value(t, ischord, unflippedlist, specs):
    # flip l because it's easier to look at it that way
    l = unflippedlist[::-1]

    rv = randint(variables.minvalue, variables.maxvalue)
    depth = notedepth(l)

    def melodicchord(rv):
        value = rv
        lastv = l[0].value

        # 3/4 are within 6, but not right next to the last note
        if myrand(3) or value == lastv:
            rd = randint(2, 6)
            if (myrand(1)):
                rd = -rd
            value = lastv + rd

        # if it is outside the range
        if (outsiderangeq(value)):
            return melodicchord(rv)
        else:
            return value

    if ('melodic' in specs['rules']) and not (ischord) and depth > 0:
        rv = melodic_value(rv, depth, specs, l)
    elif ('melodic' in specs['rules']) and ischord and not rv == "rest" and depth>0:
        rv = melodicchord(rv)
    elif ('alternating' in specs['rules']) and not (ischord) and depth > 0:
        rv = alternating_value(rv, depth, specs, l)
    elif ('alternating' in specs['rules']) and ischord and depth>0:
        rv = melodicchord(rv)

    iscopy = notecollidep(t, rv, 1, l)

    if (iscopy):
        # try again if it is a copy
        return random_value(t, ischord, l, specs)
    else:
        return rv

def random_duration(time, notelist, specs, isr):
    lv = specs["lv"]

    d = 1
    if randint(0, 50) < (lv + 2) ** 2:
        if (randint(1, 2) == 1):
            d = 2
        if (randint(0, 1000) < (lv + 2) ** 2):
            if (randint(1, 2) == 1):
                if (randint(1, 3) == 1):
                    d = 3
                else:
                    d = 4

    # so that usually it is the inverse, short notes
    if isr:
        if myrand(9):
            d = 1/d
    else:
        if myrand(2):
            d = 1 / d

    # additional chance at lower levels to be slow
    if (randint(0, 5) > lv):
        d = 2

    # rests rule
    if "rests" in specs["rules"] and not specs["lv"] in [0,1]:
        # good chance of making it half as long when bigger than 1/4
        if myrand(4) and d>0.25:
            d = d / 2
        
    # if it is on an offbeat
    if compare_around(time, 0.5):
        if (randint(0, 100) > lv ** 2):
            if (randint(1, 2) == 1):
                d = round(d-0.49)+0.5
                
    elif not compare_around(time, 0):
        remainder = time%1
        # want to fix offbeats less that 0.5 quickly
        if (randint(0, 1000) > lv ** 2):
            d = round(d-remainder+0.01)+remainder

    else:
        # if it is on the beat and it is a rest, additional chance to round it up
        if isr:
            if myrand(1):
                d = math.ceil(d-0.01)

    return d


# used to get a variation for the next round of a dance
def variation_of(old_notes, tempo):
    newnotes = variation_of_notes(old_notes)
    newb = Beatmap(tempo, newnotes)
    return newb


# future work: add the addition of chords to variation of notes
def variation_of_notes(old_notes):
    # print("called variation of notes, old notes:")
    # printnotelist(old_notes)
    # print("end of old notes")

    def random_inrange():
        return randint(variables.minvalue, variables.maxvalue)

    l = copy.deepcopy(old_notes)

    for p in range(len(l)):
        # sometimes change the value of the note, if the new value does not cause it to overlap any existing notes
        if (not myrand(4)):
            oldnote = l[p]
            newvalue = random_inrange()

            iscopy = False
            c = 0

            # check if the new value would cause it to overlap another note
            while (c < len(l)):
                # exit when beyond the place we are looking at
                if (l[c].time > l[c].time + l[p].duration):
                    break
                # don't check for overlapping if the note is the same as the one being varied
                elif (c == p):
                    pass
                elif (l[c].time + l[c].duration > oldnote.time and l[c].time < oldnote.time + oldnote.duration and l[
                    c].screenvalue() == value_to_screenvalue(newvalue)):
                    iscopy = True
                    break
                c += 1
                
            if not iscopy:
                l[p].newvalue(newvalue)

    l = shorten_doubles(l)
    return (l)

    # printnotelist(repetition(0, 1, testmap[0].notes, 5, {"rules":["repeat"]})["list"])
