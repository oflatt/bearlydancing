# random_beatmap is the entrypoint- values and durations are calculated separetly
# the note list in the end should be ordered early notes first
# notes added on generatively- each "layer" has the main melody note at the back of the list, chord notes inserted before it

from Beatmap import Beatmap
from Note import Note
from Note import value_to_screenvalue
from Note import compare_around, compare_numbers_around
import random, copy
from random import randint
import variables, math
from notelistfunctions import *
from graphics import drawthismessage

''' rule types for beatmaps (in specs)
-------- general --------------
melodic- higher chance of notes being in a row in one direction and other things
skippy- high chance of note value being 2 away, with continuing direction chance, only melodic
alternating- high chance to go back to a note or be near the previous note, and if not further away, uses melodic chords
rests- high chance of shorter notes and rests in between notes
norests- no rests are possible
nochords- no added chord notes possible
shorternotes- add more of a chance for the shorter notes

------- repeat ----------------
repeat- repeats sections with variations- all of the following can combine except repeatvalues
repeatmove- repeats sections with all the tones shifted
repeatvariation- like repeatmove but calls the variation function on repeated sectons as well (combines repeat and repeatmove)
repeatrhythm- like repeat, but uses only the times and durations for the last few notes

------ repeat separated -------
repeatvalues- like repeat, but uses only the values from last few notes and computes new durations for the values

----- modifiers ---------------
highrepeatchance- makes the initial chance for a repeat to start very high
repeatonlybeginning- makes notestoadd in repetition only take from the start of the list
repeatspaceinbetween- makes it extremely likely to repeat every other repeatlength, so that you get a repetition with normally generated notes in between
nodoublerepeats- stops one repeat repeating again

----- defaults ----------------
-If no ending specified, it throws in a tonic at the end
'''

ruletypes = ['melodic', 'skippy', 'alternating', 'rests', 'repeat',
             'repeatmove', 'repeatvariation', 'repeatvalues', 'highrepeatchance',
             'repeatrhythm', 'norests', 'nochords', 'shorternotes', 'repeatonlybeginning',
             'repeatspaceinbetween', 'nodoublerepeats']


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

    #print(str(maxval) + '  ' + str(minval) + '  ' + str(movelength))

    if outsiderangeq(maxval + movelength) or outsiderangeq(minval + movelength):
        return movednotes(l, randint(-4, 4))
    else:
        for n in l:
            n.newvalue(n.value + movelength)
        return l

def newvaluesfornotes(listofnotes, specs):
    l = copy.deepcopy(listofnotes)
    for n in l:
        n.value = random_value(n.time, n.chordadditionp, l, specs)
    return l

    
# returns a dictionary with the new time and the list
# repeatlength is the number of notes to repeat
# movelength is an offset for values of notes
# startingtime is the time the main loop left off
# maxtime is the (soft) limit on time to use
def repetition(time, movelength, listofnotes, repeatlength, specs, maxtime):
    if variables.devmode:
        print('repetition: time: ' + str(time) + ' repeatlength: ' +
              str(repeatlength) + ' last note time: ' + str(listofnotes[-1].time) + ' depth: ' + str(notedepth(listofnotes)))
    if 'repeatvalues' in specs['rules']:
        return repeatvaluesrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime)
    else:
        return normalrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime)

def repeatvaluesrepetition(starttime, movelength, listofnotes, repeatlength, specs, maxtime):
    l = listofnotes.copy()

    # get the last repeatlength notes to add on again
    notestoadd = getlastnlayers(l, repeatlength)
    
    valuelist = valuelistfromnotesskipchords(notestoadd)
    valuelistoriginal = valuelist.copy()
    
    time = starttime
    iterations = 0
    
    while len(valuelist) > 0:
        addl = addlayer(l, time, specs, valuelist)
        l = addl[0]
        time += addl[1]

        # chance to do it again
        if len(valuelist) == 0 and time<maxtime:
            if iterations == 0:
                if myrand(2):
                    valuelist = valuelistoriginal.copy()
                    iterations += 1
            else:
                if myrand(1):
                    valuelist = valuelistoriginal.copy()
                    iterations += 1
            

    return {'time': time, 'list':l}

# iterations is the number of times it has recursively called itself
def normalrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime, iterations = 0):
    l = listofnotes.copy()

    # get the last repeatlength notes to add on again
    if not 'repeatonlybeginning' in specs['rules']:
        notestoadd = getlastnlayers(l, repeatlength)
    else:
        notestoadd = getfirstnlayers(l, repeatlength)
        
    notestoadd = copy.deepcopy(notestoadd)
        
    
    # with certain rules we want to call variation of notes on the list
    if 'repeatvariation' in specs['rules']:
        notestoadd = variation_of_notes(notestoadd)

    if 'repeatmove' in specs['rules']:
        if variables.devmode and iterations == 0:
            print("movelength: " + str(movelength))
        notestoadd = movednotes(notestoadd, movelength)

    if 'repeatrhythm' in specs['rules']:
        notestoadd = newvaluesfornotes(notestoadd, specs)

    oldendtime = time
    if 'repeatonlybeginning' in specs['rules']:
        oldendtime = notestoadd[-1].time + notestoadd[-1].duration
    
    # calculate when to start next note so that the first note is on the same part of the beat as it was
    newstarttime = time + abs(time%1 - notestoadd[0].time%1)
    offsetfactor = newstarttime - notestoadd[0].time

    # offset the notestoadd by the offsetfactor
    for n in notestoadd:
        n.time += offsetfactor

    newtime = oldendtime+offsetfactor

    l.extend(notestoadd)

    # chance to repeat section moved again
    if newtime<maxtime and not 'nodoublerepeats' in specs['rules']:
        returnval = {'time': newtime, 'list': l}
        doanotherp = False
        # if we have already added an extra
        if iterations > 0:
            if myrand(1):
                doanotherp = True
        else:
            if myrand(2):
                doanotherp = True
                
        if doanotherp:
            returnval = normalrepetition(newtime, movelength, l, repeatlength, specs, maxtime, iterations+1)
        else:
            if variables.devmode:
                print(str(iterations+1) + " times")
        return returnval
    else:
        if variables.devmode:
            print(str(iterations+1) + " times")
        return {'time': newtime, 'list': l}


# returns if there should be a repetition
def repeatp(notelist, repeatlength, specs):
    l = notelist
    depth = notedepth(l)
    if 'repeatspaceinbetween' in specs['rules']:
        # if on the every other one, the even dividing by repeatlength, very high chance
        if((len(notelist)/repeatlength) % 2 < 1):
            repeatp = randint(-2, depth%repeatlength) == 0
        else:
            repeatp = randint(-6, depth%repeatlength) == 0
    elif 'highrepeatchance' in specs['rules']:
        repeatp = randint(-1, depth%repeatlength) == 0
    else:
        repeatp = randint(-2, depth % repeatlength) == 0

    repeatp = repeatp and depth>=repeatlength
        
    return repeatp

def repeatlengthfromspecs(specs):
    lv = specs['lv']
    # repeatlength used in repeat rule for how many notes back to copy
    if 'repeatvalues' in specs['rules'] or 'repeatrhythm' in specs['rules']:
        return randint(2, 4+int(lv/3))
    else:
        rlength = randint(3, 5)
        if not myrand(4):
            rlength += randint(0, 4)
            
        if myrand(2):
            rlength += int(randint(0, lv)/2)

        # make 3 not very likely
        if rlength < 4:
            if myrand(2):
                rlength += 1
                
        if rlength%2 == 1:
            if myrand(1):
                rlength += 1
        return rlength
    
# returns a tuple with a new list and the duration of the new note
# values touse is a list of values to use instead of calling random_value
def addnote(notelist, time, ischord, specs, valuestouse):
    lv = specs['lv']
    l = notelist.copy()
    duration = random_duration(time, l, specs, False, ischord)
    # if it is a chord, chance that the duration is the same as the melody
    if ischord:
        if randint(0, 100) > ((lv/1.8) + 2) ** 2:
            duration = l[-1].duration

    # so you can specify a value
    if len(valuestouse)==0:
        rv = random_value(time, ischord, l, specs)
    else:
        if notecollidep(time, valuestouse[0], duration, l):
            rv = random_value(time, ischord, l, specs)
        else:
            # pop off the first value on the list so that it is not used again
            rv = valuestouse.pop(0)
        
    # chord notes added before the main note to make it easier to compare to the melody
    if ischord:
        l.insert(len(l) - 1, Note(rv, time, duration, True))
    else:
        l.append(Note(rv, time, duration))

    return (l, duration)

# returns a new list and the duration of the layer in a tuple
# valuestouse is a list of values to use instead of calling random_value, for use in repeatvaluesrepetition
def addlayer(notelist, time, specs, valuestouse = []):
    lv = specs['lv']
    isr = restp(time, notelist, specs)

    if isr:
        return (notelist, random_duration(time, notelist, specs, True, False))
    else:
        oldt = time
        notedurations = []
        addn = addnote(notelist, oldt, False, specs, valuestouse)
        l = addn[0]
        notedurations.append(addn[1])

        def addchord():
            # don't pass in valuestouse for chords
            addn = addnote(l, oldt, True, specs, [])
            notedurations.append(addn[1])
            return addn[0]

        # chance to add chord notes, if it is not a rest
        if (randint(0, 150) < ((lv/2) + 2) ** 2) and not 'nochords' in specs['rules']:
            if randint(1, 3) == 1:
                l = addchord()
            if randint(0, 1000) < (lv + 2) ** 2 and random.random() < 0.5:
                l = addchord()
            # and one more blanket small chance to add a note
            if not myrand(40):
                l = addchord()

        return (l, max(notedurations))

def random_beatmap(specs):
    if variables.devmode:
        print()
        print('output of:')
        print("   " + str(specs['rules']) + " lv: " + str(specs['lv']))
        print()

    # first update the screen to say it is being generated
    drawthismessage("generating new beatmap")
    variables.updatescreen()
    # set the variable so that time stops for a frame
    variables.generatingbeatmapp = True
    
    variation_of_notes([])
    l = []
    lv = specs['lv']
    maxtime = specs['maxtime']
    maxtime = maxtime + lv * 2
    time = 1
    # repeatlength used in repeat rule for how many notes back to copy
    repeatlength = None
    repeatmodep = False
    for r in specs['rules']:
        if r[0:6] == 'repeat':
            repeatmodep = True
            repeatlength = repeatlengthfromspecs(specs)
            break

    # masterloop for adding on notes
    while time < maxtime:
        addlayerp = False
        if repeatmodep:
            # chance to do a repetition
            if repeatp(l, repeatlength, specs):
                # add on the last repeatlength notes again, varied
                r = repetition(time, randint(-4, 4), l, repeatlength, specs, maxtime)
                l = r['list']
                time = r['time']
            else:
                addlayerp = True
        else:
            addlayerp = True
            
        if addlayerp:
            addl = addlayer(l, time, specs)
            l = addl[0]
            time += addl[1]

    # default cheap ending- throw in a tonic at end
    lastvalue = random.choice([variables.minvalue, variables.maxvalue, 0])
    startt = round(l[-1].time + l[-1].duration + 0.5)
    l.append(Note(lastvalue, startt, randint(1,2)))

    # tempo is milliseconds per beat
    tempo = (1200 * 3) / (math.sqrt(lv)*0.4+ 0.08*lv + 3.5)

    if variables.devmode:
        printnotelist(l)

    # then perform checks
    if not notetimeorderedp(l):
        thrownoteerror('note list not ordered properly for time')
    if not notechordorderedp(l):
        thrownoteerror('note list not ordered properly for chords')
    if anynotescollide(l):
        thrownoteerror('notes collided')

    for rule in specs['rules']:
        if not rule in ruletypes:
            thrownoteerror('rule ' + str(rule) + ' unknown')
        
    return Beatmap(tempo, l)


# assume depth>0
def melodic_value(rv, depth, specs, l):
    value = rv
    lastv = l[-1].value

    # have a big chance of 2 away if 'skippy' rule is on
    if ('skippy' in specs['rules']) and myrand(3):
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

    # 2/3 * 3/4 chance of being 1 or 2 away from previous note
    elif myrand(2) and myrand(3):
        # 2/3 chance of continuing same direction
        if (depth > 1):
            secondv = random_last(1, l).value
            if ((lastv - 1 == secondv or lastv + 1 == secondv) and myrand(2)):
                value = lastv + (lastv - secondv) * random.choice([1,1,2])
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

    #1/3 chance to be within 6
    elif not myrand(2):
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
        #print('non')
        distance_away = 0
        if myrand(1):
            distance_away = randint(3, 5)
        elif myrand(1):
            distance_away = randint(4, 6)
        elif myrand(1):
            #print('far')
            distance_away = randint(1, 7)

        if myrand(1):
            distance_away = -distance_away

        startingpoint = rv
        if depth>1 and myrand(1):
            startingpoint = lastv

        if (distance_away != 0):
            if outsiderangeq(startingpoint + distance_away):
                return not_alternating()
            else:
                return startingpoint + distance_away
        else:
            return startingpoint

    if depth > 1:
        secondv = random_last(1, l).value
        # if we actually do a alternation
        if myrand(4) and lastv != secondv:
            #print("alternation")
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
    if (len(l) > 0) and not 'norests' in specs['rules']:
        # if the last note was not a rest
        if ('rests' in specs['rules'] and l[-1].time + l[-1].duration >= t-0.05):
            if compare_around(t, 0):
                if not myrand(2):
                    isr = True
            else:
                # if not on the beat very high chance of a rest if the last note was not a rest
                if (myrand(5)):
                    isr = True
                    
        # 1/9 is a rest if not rests rule
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

        # half are thirds or fifths
        if myrand(1):
            rd = random.choice([-2, 2, -4, 4])
            value = lastv+rd
        # 2/3 of remaining are not right next to the last note
        elif myrand(2) or value == lastv:
            rd = randint(2, 5)
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
    elif ('melodic' in specs['rules']) and ischord and not rv == 'rest' and depth>0:
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

def random_duration(time, notelist, specs, isr, ischord):
    lv = specs['lv']
    if 'shorternotes' in specs['rules']:
        lv *= 6/5

    def halfp():
        offset = lv/200
        if 'shorternotes' in specs['rules']:
            offset = 0.2 + lv/100 
        return random.random() < 0.5+offset

    d = 1
    if randint(0, 50) < (lv + 2) ** 2:
        if halfp():
            d = d*2
        if (randint(0, 1000) < min((lv + 2) ** 2, 600+lv)):
            if halfp():
                d = d*2

    # chance for triplet
    if randint(0, 1000) < (lv + 10) ** 2:
        if not myrand(9):
            d = 3
                
    # so that usually it is the inverse, short notes
    if random.random() < (2/3) + min(2/9, lv/20):
        d = 1 / d

    # so we don't end up with long notes for higher levels
    if lv > 10 and d>2:
        d -= 1
    if lv > 10 and d==2:
        if myrand(1):
            d -= 1

    # chance for triplet if last one was a triplet (and short)
    if len(notelist) > 0:
        if compare_numbers_around(notelist[-1].duration, 1/3) and (compare_around(time, 2/3) or compare_around(time, 1/3)):
            if myrand(3):
                d = 1/3

    # additional chance at lower levels to be slow
    if (randint(0, 7) > lv):
        d = 2

        
    # rests rule
    if 'rests' in specs['rules'] and not specs['lv'] in [0,1]:
        # good chance to make it half as long
        if myrand(4) and d>0.25:
            d = d / 2
        
    # if it is on an offbeat
    if compare_around(time, 0.5):
        # two third chance to get over level barrior if lv too high
        if (randint(0, 200) > lv ** 2) or myrand(2):
            if myrand(3):
                d = round(d-0.52)+0.5

    elif not compare_around(time, 0):
        remainder = time%1
        # high chance of making the duration of the next note another of the same kind of unit
        if myrand(3):
            d = min(remainder, 1-remainder)
        # otherwise we want to fix offbeats less that 0.5 quickly
        elif (randint(0, 1000) > lv ** 2):
            d = round(d-remainder+0.01)+remainder

    # else it is on the beat
    else:
        # if it is on the beat and it is a rest, additional chance to round it up
        if isr:
            if myrand(1):
                d = math.ceil(d-0.01)

    # rests rule and it is a rest
    if 'rests' in specs['rules'] and isr:
        if compare_around(time, 0):
            if not myrand(2):
                d = notelist[-1].duration
        # if off beat, good chance of the same length as the previous note
        elif myrand(5):
            d = notelist[-1].duration

    if ischord:
        # if it is a chord, big chance to simply be the same duration as the melody
        if myrand(4):
            d = notelist[-1].duration
            
    return d


# used to get a variation for the next round of a dance
def variation_of(old_notes, tempo):
    newnotes = variation_of_notes(old_notes)
    newb = Beatmap(tempo, newnotes)
    return newb


# future work: add the addition of chords to variation of notes
def variation_of_notes(old_notes):
    # print('called variation of notes, old notes:')
    # printnotelist(old_notes)
    # print('end of old notes')

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
            potentialreplace = copy.copy(oldnote)
            potentialreplace.newvalue(newvalue)
            iscopy = notecollidebesidesselfp(potentialreplace, l)
                
            if not iscopy:
                l[p].newvalue(newvalue)

    return (l)

