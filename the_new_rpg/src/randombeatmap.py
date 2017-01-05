from Beatmap import Beatmap
from Note import Note
from Note import value_to_screenvalue
import random, copy
from random import randint
import variables

'''rule types for beatmaps
skippy- high chance of note being 2 away, with continuing direction chance, only with melodic
alternating- high chance to go back to a note or be near the previous note, and if not further away, uses melodic chords
repeat- repeats a melody with variations
cheapending- pick a random tonic and throw it on the end
rests- high chance of shorter notes and rests in between notes
'''
testmapa = [Beatmap((1200 * 3) / 4, [Note(-7, 2, 2), Note(-6, 1, 1)])]
testmapb = [Beatmap((1200 * 3) / 4, [Note(0, 1, 1), Note(0, 4, 1), Note(0, 5, 1), Note(1, 6, 1)])]
testmap = [Beatmap((1200 * 3) / 4, [Note(0, 1, 0.9), Note(-1, 2, 1), Note(8, 3, 1), Note(14, 5, 1), Note(-7, 6, 1)])]


# if n is 2, then there is a 2/3 chance of true
def myrand(n):
    if (randint(0, n) < n):
        return True
    else:
        return False


# q stands for question mark
def outsiderangeq(value):
    return value < variables.minvalue or value > variables.maxvalue


def shorten_doubles(l):
    newl = l
    x = 0
    while (x < len(l)):
        y = 1
        while x + y < len(l):
            if l[x + y].time <= l[x].time + l[x].duration:
                if l[x].screenvalue == l[x + y].screenvalue:
                    newl[x].duration -= 0.1
                    break
            else:
                break
            y += 1
        x += 1
    return newl


def random_beatmap(specs):
    print(specs["rules"])
    l = []
    lv = specs["lv"]
    maxtime = specs["maxtime"]
    maxtime = maxtime + lv * 2

    def addnote(time, ischord):
        duration = rand_duration(time, l, specs)
        rv = random_value(time, ischord, l, specs)
        # if it is not a rest
        if (not rv == "rest"):
            if (ischord):
                l.insert(len(l) - 1, Note(rv, time, duration))
            else:
                l.append(Note(rv, time, duration))
        return duration

    time = 1
    # repeatlength used in repeat rule for how many notes back to copy
    repeatlength = randint(3, 7 + lv)

    def repitition():
        # add on the last repeatlength notes again, varied
        notestoadd = variation_of_notes(l[-repeatlength:len(l)])
        timedifference = notestoadd[-1].time - notestoadd[0].time
        for n in notestoadd:
            n.time += timedifference
        l.extend(notestoadd)

        maxduration = notestoadd[-1].duration

        for g in notestoadd:
            if (g.time >= notestoadd[-1].time and g.duration > maxduration):
                maxduration = g.duration

        return timedifference + maxduration

    def normalloop():
        oldt = time
        notedurations = []
        notedurations.append(addnote(oldt, False))
        # chance to add more notes at the same time
        if (randint(0, 100) < (lv + 2) ** 2):
            if randint(1, 2) == 1:
                notedurations.append(addnote(oldt, True))
            if randint(0, 1000) < (lv + 2) ** 2:
                notedurations.append(addnote(oldt, True))
        return max(notedurations)

    while time < maxtime:
        if ("repeat" in specs["rules"]):
            # if we do a repitition
            if (randint(-1, len(l) % repeatlength) == 0 and len(l) >= repeatlength):
                # add on the last repeatlength notes again, varied
                print('do repitition')
                time += repitition()
            else:
                time += normalloop()
        else:
            time += normalloop()

    if ("cheapending" in specs["rules"]):
        lastvalue = random.choice([variables.minvalue, variables.maxvalue, 0])
        startt = l[-1].time + l[-1].duration
        l.append(Note(lastvalue, startt, 1 + (1 - startt % 1)))

    tempo = (1200 * 3) / ((lv / 3) + 3.5)
    l = shorten_doubles(l)
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
            print("back1")
            # 2/3 chance to go back one note
            if (myrand(2)):
                value = lastv - 1
        elif (lastv < secondv - 2):
            print("back1")
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
        print("non")
        distance_away = 0
        if myrand(1):
            distance_away = randint(3, 5)
        elif myrand(1):
            distance_away = randint(4, 6)
        elif myrand(1):
            print('far')
            distance_away = randint(1, 7)

        if myrand(1):
            distance_away = -distance_away

        if (distance_away != 0):
            if outsiderangeq(rv + distance_away):
                return not_alternating()
            else:
                return rv + distance_away
        else:
            print('lerandom')
            return rv

    if depth > 1:
        secondv = random_last(1, l).value
        # if we actually do a alternation
        if myrand(4) and lastv != secondv:
            # half chance to pick same secondv note
            if myrand(1):
                print('same')
                value = secondv
            # otherwise pick a note close to it
            else:
                # within one
                if myrand(3):
                    print("within 1")
                    value = secondv + random.choice([1, -1])
                # otherwise within 2
                else:
                    print('within 2')
                    value = secondv + random.choice([1, 2, -1, -2])
        else:
            value = not_alternating()
    else:
        value = not_alternating()

    if outsiderangeq(value):
        return alternating_value(rv, depth, specs, l)
    else:
        return value


def random_value(t, ischord, list, specs):
    # flip l because it's easier to look at it that way
    l = list[::-1]

    rv = randint(variables.minvalue, variables.maxvalue)
    depth = notedepth(l)

    # handeling rests, 8/9 times it will be a note
    if ("melodic" in specs["rules"]):
        if not myrand(8):
            rv = "rest"

    def melodicchord(rv):
        value = rv
        lastv = l[0].value

        # 3/4 are within 6
        if (myrand(3)):
            rd = randint(1, 6)
            if (myrand(1)):
                rd = -rd
            value = lastv + rd

        # if it is outside the range
        if (outsiderangeq(value)):
            return melodicchord(rv)
        else:
            return value

    if not rv == "rest":
        if ('melodic' in specs['rules']) and not (ischord) and depth > 0:
            rv = melodic_value(rv, depth, specs, l)
        elif ('melodic' in specs['rules']) and ischord and not rv == "rest":
            rv = melodicchord(rv)
        elif ('alternating' in specs['rules']) and not (ischord) and depth > 0:
            rv = alternating_value(rv, depth, specs, l)
        elif ('alternating' in specs['rules']) and ischord:
            rv = melodicchord(rv)

    iscopy = False
    if (not rv == "rest"):
        # make sure the value does not overlap another one
        x = 0
        while (x < len(l)):
            if (l[x].time + l[x].duration > t and l[x].screenvalue == value_to_screenvalue(rv)):
                iscopy = True
                break
            x += 1

    if (iscopy):
        # try again if it is a copy
        return random_value(t, ischord, l, specs)
    else:
        return rv


def rand_duration(time, list, specs):
    lv = specs["lv"]
    # flip it so we can look at it more easily
    l = list[::-1]

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

    # additional chance at lower levels to be slow
    if (randint(0, 5) > lv):
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


def variation_of(old_notes, tempo):
    return Beatmap(tempo, variation_of_notes(old_notes))


def variation_of_notes(old_notes):
    print("called variation of notes")
    for a in old_notes:
        print("value: " + str(a.value) + "time: " + str(a.time))

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
                    c].screenvalue == value_to_screenvalue(newvalue)):
                    iscopy = True
                    break
                c += 1

            if not iscopy:
                l[p] = Note(newvalue, oldnote.time, oldnote.duration)

    l = shorten_doubles(l)
    return (l)
