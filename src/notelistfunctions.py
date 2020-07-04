import variables, random, devoptions
from Note import compare_numbers_around
from Note import Note

from random import randint

ruletypes = ['melodic', 'skippy', 'alternating', 'rests', 'repeat',
             'repeatmove', 'repeatvariation', 'repeatvalues', 'highrepeatchance',
             'repeatrhythm', 'norests', 'nochords', 'shorternotes', 'repeatonlybeginning',
             'repeatspaceinbetween', 'nodoublerepeats', 'noaccidentals',
             'highervalues', 'lowervalues',
             'seperatedchordchance',
             'holdlongnote', 'doublenotes', 'combinemelodies']

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
        if l[x].getscreenvalue() == Note.value_to_screenvalue(nvalue):
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
            if l[x].getscreenvalue() == Note.value_to_screenvalue(nvalue):
                if l[x].time+l[x].duration > ntime and l[x].time < ntime+nduration:
                    note.collidedwithanotherp = True
                    iscopy = True
                    break
        x += 1
    return iscopy

# none if no notes collide
def anynotescollide(notelist):
    collisionp = None
    for n in notelist:
        if notecollidebesidesselfp(n, notelist):
            collisionp = n.time
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
        
        # if it should have been a chord addition note
        if n.time == l[i+1].time and not n.chordadditionp:
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

def notevaluesintegersp(l):
    for n in l:
        if not isinstance(n.value, int):
            return False
    return True

def notedurationsmatchp(l, num):
    for n in l:
        if not n.duration == num:
            return False
    return True

def notevaluesvalidp(l):
    for n in l:
        if outsiderangeq(n.value):
            return False
    return True

# None if no chords have a number of notes greater than chordsize
def haschordsgreaterthan(l, chordsize):
    counter = 0
    lasttime = None
    for n in l:
        if lasttime != None:
            if compare_numbers_around(n.time, lasttime):
                counter += 1
            else:
                counter = 1
        if counter > chordsize:
            return lasttime
        lasttime = n.time
    return None

def performnotelistchecks(l):
    if not notetimeorderedp(l):
        thrownoteerror('note list not ordered properly for time')
    if not notechordorderedp(l):
        thrownoteerror('note list not ordered properly for chords')
    collide = anynotescollide(l)
    if collide != None:
        thrownoteerror('notes collided at time ' + str(collide))
    if not noteaccidentalsconsistantp(l):
        thrownoteerror('accidental note at same time as non accidental')
    if not notevaluesintegersp(l):
        thrownoteerror('not all values in note list were integers')
    if not notevaluesvalidp(l):
        thrownoteerror('not all not values were valid, one was outside of range.')


def performdancepadmodenotelistchecks(l):
    if not notedurationsmatchp(l, 1):
        thrownoteerror('not all durations for notes were 1 in dance pad mode')
    chordcheck = haschordsgreaterthan(l, 2)
    if chordcheck != None:
        thrownoteerror('there exists a chord with more then 2 notes in it at time ' + str(chordcheck) + ' in dance pad mode, which is impossible to play.')


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
                if l[x].getscreenvalue() == l[x + y].getscreenvalue():
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


# loops through the lists simultaneously, building a new list with notes from chordl added if they don't collide
# assumes both lists are time ordered
def combineaschords(firstlist, chordlist):
    l = []
    firstindex = 0
    secondindex = 0

    while firstindex < len(firstlist) and secondindex < len(chordlist):
        note1 = firstlist[firstindex]
        note2 = chordlist[secondindex]
        if note1.time < note2.time:
            l.append(note1)
            firstindex += 1
        elif note1.time > note2.time:
            if not notecollidep(note2.time, note2.value, note2.duration, firstlist):
                l.append(note2)
            
            # maintain chord ordered
            if l[-1].time == l[-2].time:
                l[-2].chordadditionp = True
                l[-1].chordadditionp = False

            secondindex += 1
        else:
            l.append(note1)
            firstindex += 1
            if not notecollidep(note2.time, note2.value, note2.duration, firstlist):
                l.insert(-1,note2)
                note2.chordadditionp = True
            secondindex += 1

    # now add on the rest of the notes
    if firstindex < len(firstlist):
        l.extend(firstlist[firstindex:])

    # add on rest of chord list
    while secondindex < len(chordlist):
        note2 = chordlist[secondindex]
        if not notecollidep(note2.time, note2.value, note2.duration, firstlist):
            l.append(note2)
        
        # maintain chord ordered
        if l[-1].time == l[-2].time:
            l[-2].chordadditionp = True
            l[-1].chordadditionp = False

        secondindex += 1

    return l

def checkexpectnotelist(got, expected, errormessage):
    if not len(got) == len(expected):
        print("Error- different lengths: " + errormessage)
        print("expected")
        printnotelist(expected)
        print("got")
        printnotelist(got)
    else:
        for a in range(len(expected)):
            if not result[a].equalp(expected[a]):
                print("Error: " + errormessage + "at time " + str(expected[a].time))
                print("expected")
                printnotelist(expected)
                print("got")
                printnotelist(got)

# test combining lists
if devoptions.devmode:
    testl = [Note(2, 0, 2), Note(3, 2, 1)]
    testchordl = [Note(7, 2, 2, chordadditionp = True), Note(3, 2, 4), Note(8, 8, 8)]
    
    expected = [Note(2,0,2), Note(7, 2, 2, chordadditionp = True), Note(3, 2, 1), Note(8,8,8)]
    result = combineaschords(testl, testchordl)
    checkexpectnotelist(result, expected, "combineaschordstest1")

    testl = [Note(1, 0, 1), Note(1, 2, 1)]
    testchordl = [Note(2, 0, 1)]
    result = combineaschords(testl, testchordl)
    expected = [Note(2, 0, 1, chordadditionp = True), Note(1, 0, 1), Note(1, 2, 1)]
    checkexpectnotelist(result, expected, "combineaschordstest2")
    
