import variables, random
from Note import value_to_screenvalue
from Note import compare_numbers_around
from Note import Note

from random import randint

ruletypes = ['melodic', 'skippy', 'alternating', 'rests', 'repeat',
             'repeatmove', 'repeatvariation', 'repeatvalues', 'highrepeatchance',
             'repeatrhythm', 'norests', 'nochords', 'shorternotes', 'repeatonlybeginning',
             'repeatspaceinbetween', 'nodoublerepeats', 'noaccidentals']

def hasrule(rule, specs):
    if not rule in ruletypes:
        raise ValueError("rule " + rule + " does not exist")
    else:
        return rule in specs['rules']

# if n is 2, then there is a 2/3 chance of true
def myrand(n):
    if random.random() < n/(n+1):
        return True
    else:
        return False


def printnotelist(l):
    for x in l:
        isc = ""
        if x.chordadditionp:
            isc = " +chordaddition"
        if x.collidedwithanotherp:
            isc = isc + " +COLLIDED"
        print("value: " + str(x.value) + " time: " + str(x.time) + " duration: " + str(x.duration) + isc)


# returns how 'deep' a list is, how many layers of time it has
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

# random last is to get a random not of the ones last added, so that we don't compare parts of a chord
# depth is how many layers of times for notes we remove
# l is a list of notes where the earlier ones have later times, (flipped list)
def random_last(depth, l):
    # removed is how far in the list to go to get the note
    removed = 0
    # first remove layers to satify depth
    for inotused in range(depth):
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

testl = [Note(5, 1, 2), Note(6, 2, 1), Note(6, 4, 1), Note(2, 5, 2), Note(3, 6, 4),
         Note(4, 7, 3), Note(4, 7, 3)]


# print(random_last(0, testl).value)
# print(random_last(1, testl).value)

# returns a list of the notes for the first layer, the one most recent in time
# a layer is notes that share the same time, so a melody note and its chords
def getfirstlayer(notelist, startingpoint = 0):
    l = []
    i = len(notelist) - 1 - startingpoint
    layertime = notelist[i].time
    while i >= 0:
        if compare_numbers_around(notelist[i].time, layertime):
            l.insert(0,notelist[i])
        else:
            break
        i -= 1
    return l

def getnoteswithintime(notelist, starttime, endtime):
    l = []
    for n in notelist:
        if n.time >= starttime and n.time <= endtime:
            l.append(n)
    
    return l

# notelist is ordered early notes first
# startingpoint in these funcions is how many notes to skip, not layers
# skiplayers is how many layers back to skip before starting to take layers
def getlastnlayers(notelist, n, startingpoint = 0, skiplayers = 0):
    i = startingpoint
    l = []
    toskip = skiplayers
    layers = 0
    while i <= len(notelist)-1 and layers<n:
        nextlayer = getfirstlayer(notelist, i)

        if toskip <=0:
            layers += 1
            l = nextlayer + l
        else:
            toskip -= 1
        
        i += len(nextlayer)

    return l

def getfirstnlayers(notelist, n, startingpoint = 0):
    l = notelist.copy()
    l.reverse()
    newl = getlastnlayers(l, n, startingpoint)
    newl.reverse()
    return newl


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

def notecollidebesidesselfp(note, l):
    ntime = note.time
    nduration = note.duration
    nvalue = note.value
    
    iscopy = False
    x = 0
    while (x < len(l)):
        if not note == l[x]:
            if l[x].screenvalue() == value_to_screenvalue(nvalue):
                if l[x].time+l[x].duration > ntime and l[x].time < ntime+nduration:
                    note.collidedwithanotherp = True
                    iscopy = True
                    break
        x += 1
    return iscopy

def anynotescollide(notelist):
    collisionp = False
    for n in notelist:
        if notecollidebesidesselfp(n, notelist):
            collisionp = True
            break
    return collisionp

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
        # if it should have been a chord addition note
        elif n.time == l[i+1].time:
            orderedp = False
            break
    return orderedp

# checks to make sure when one note is an accidental, all other notes at that time are also accidentals
def noteaccidentalsconsistantp(l):
    for i in range(len(l)-1):
        n = l[i]
        n2 = l[i+1]
        # if they are at the same time
        if compare_numbers_around(n.time, n2.time, 0.05):
            if not n.accidentalp == n2.accidentalp:
                return False
    return True

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

def valuelistfromnotes(notelist):
    vlist = []
    for n in notelist:
        vlist.append(n.value)

    return vlist

def valuelistfromnotesskipchords(notelist):
    vlist = []
    for n in notelist:
        if not n.chordadditionp:
            vlist.append(n.value)
    return vlist

# does not copy notes
def listskipchords(notelist):
    l = []
    for n in notelist:
        if not n.chordadditionp:
            l.append(n)
    return l
