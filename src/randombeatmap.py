# random_beatmap is the entrypoint- values and durations are calculated separetly

#    contracts
# the note list in the end should be ordered early notes first
# notes added on generatively- each "layer" has the main melody note at the end of the list, chord notes inserted before it
# no note should have a time plus duration longer than current time
from Beatmap import Beatmap
from Note import Note
from Note import value_to_screenvalue
from Note import compare_around, compare_numbers_around
from notelistvariation import variation_of_notes
from notelistfunctions import *
from graphics import drawthismessage
from notelistrepetition import repetition, repeatp, repetitiondepth, getrepeatduration
from notelistrandomvalue import random_value

import random, copy
from random import randint
import variables, math


''' rule types for beatmaps (in specs)
-------- general --------------
melodic- higher chance of notes being in a row in one direction and other things
skippy- high chance of note value being 2 away, with continuing direction chance, only melodic
alternating- high chance to go back to a note or be near the previous note, and if not further away, uses melodic chords
rests- high chance of shorter notes and rests in between notes
norests- no rests are possible
nochords- no added chord notes possible
shorternotes- add more of a chance for the shorter notes
highervlaues- bias values higher
lowervalues- bias values lower
seperatedchordchance- chance to have a rest and then a chord with three notes in it

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
repeatspaceinbetween- makes it extremely likely to repeat every other repeatduration, so that you get a repetition with normally generated notes in between
nodoublerepeats- stops one repeat repeating again
noaccidentals- makes no "modified" notes, no accidentals that are one pitch above


----- defaults ----------------
-If no ending specified, it throws in a tonic at the end
'''


testmapa = [Beatmap((1200 * 3) / 4, [Note(-7, 2, 2), Note(-6, 1, 1)], variables.generic_specs)]
testmap = [Beatmap((1200 * 3) / 4, [Note(0, 1, 0.2), Note(0, 1.3, 0.1), Note(0, 2, 0.4), Note(0, 2.5, 0.4), Note(0, 3, 0.4),
                                    Note(0, 3.5, 0.4), Note(0, 4, 0.4), Note(0, 4.5, 0.4), Note(0, 5, 0.4), Note(0, 5.5, 0.4),
                                    Note(0, 6, 0.4), Note(0, 6.5, 0.4), Note(0, 7, 0.4), Note(0, 7.5, 0.4), Note(0, 8, 0.4)], variables.generic_specs)]


def makeaccidentalp(specs, l):
    if hasrule("noaccidentals", specs):
        return False
    
    lv = specs['lv']
    athreshhold = variables.accidentallvthreshhold
    # only make accidentals on beatmaps of lv 8 or higher 
    if lv<athreshhold:
        return False
    else:
        chancemultiplier = 1
        notestocheck = 8
        accidentalcounter = 0
        # get how many accidentals were in the past 8 notes
        for i in range(min(8, len(l))):
            if l[-i].accidentalp:
                accidentalcounter += 1
        chancemultiplier -= (1/(notestocheck)) * accidentalcounter
        levelchance = min(1/3, (math.pow(lv-athreshhold, 0.7)+1)/40)
        return random.random() < levelchance*chancemultiplier

        
# returns a tuple with a new list and the duration of the new note
# values touse is a list of values to use instead of calling random_value
def addnote(notelist, time, ischord, specs, valuestouse, accidentalp):
    lv = specs['lv']
    l = notelist.copy()
    duration = random_duration(time, l, specs, False, ischord)


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
        l.insert(len(l) - 1, Note(rv, time, duration, True, accidentalp = accidentalp))
    else:
        l.append(Note(rv, time, duration, accidentalp = accidentalp))

    return (l, duration)

# returns none if not a special layer, otherwise returns a new list and duration of the layer in a tuple
def speciallayer(notelist, time, specs):

    if hasrule("seperatedchordchance", specs) and not myrand(4+specs['lv']/2):
        notelist = notelist.copy()
        restdur = random_duration(time, notelist, specs, True, False)
        notedur = random_duration(time, notelist, specs, False, False)
        val1 = random_value(time+restdur, False, notelist, specs)
        notelist.append(Note(val1, time+restdur, notedur, False))
        val2 = random_value(time+restdur, True, notelist, specs)
        notelist.insert(-1, Note(val2, time+restdur, notedur, True))
        val3 = random_value(time+restdur, True, notelist, specs)
        notelist.insert(-1, Note(val3, time+restdur, notedur, True))
        return (notelist, restdur+notedur)

    return None


# returns a new list and the duration of the layer in a tuple
# valuestouse is a list of values to use instead of calling random_value, for use in repeatvaluesrepetition
def addlayer(notelist, time, specs, valuestouse = []):
    lv = specs['lv']
    isr = restp(time, notelist, specs)

    # if there is a special layer, do that instead
    if len(valuestouse) == 0:
        sl = speciallayer(notelist, time, specs)
        if sl != None:
            return sl
    
    if isr:
        return (notelist, random_duration(time, notelist, specs, True, False))
    else:
        accidentalp = makeaccidentalp(specs, notelist)
        oldt = time
        notedurations = []
        addn = addnote(notelist, oldt, False, specs, valuestouse, accidentalp)
        l = addn[0]
        notedurations.append(addn[1])

        def addchord():
            # don't pass in valuestouse for chords
            addn = addnote(l, oldt, True, specs, [], accidentalp)
            notedurations.append(addn[1])
            return addn[0]

        # chance to add chord notes, if it is not a rest
        if (randint(0, 150) < ((lv/2) + 2) ** 2) and not hasrule('nochords',specs):
            if randint(1, 3) == 1:
                l = addchord()
            if randint(0, 1000) < (lv + 2) ** 2 and random.random() < 0.5:
                l = addchord()
            # and one more blanket small chance to add a note
            if not myrand(40):
                l = addchord()

        return (l, max(notedurations))

def maxtimefromspecs(specs):
    maxtime = specs['maxtime']
    return maxtime + specs['lv']*2

    
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
    
    l = []
    lv = specs['lv']
    maxtime = maxtimefromspecs(specs);
    time = 0
    # repeatduration used in repeat rule for how much time back to copy
    repeatduration = None
    repeatmodep = False
    for r in specs['rules']:
        if r[0:6] == 'repeat':
            repeatmodep = True
            break

    # masterloop for adding on notes
    while time < maxtime:
        addlayerp = False
        if repeatmodep:
            # chance to do a repetition
            if repeatp(l, specs, time, maxtime):
                # how many layers of notes to skip before the area of notes being repeated
                repeatduration = getrepeatduration(l, specs, maxtime, time)
                skipdepth = repetitiondepth(l, repeatduration, specs, maxtime, time)
                # repetition entry
                # add on the last repeatduration notes again, varied
                r = repetition(time, randint(-4, 4), l, repeatduration, specs, maxtime, skipdepth)
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
    if not noteaccidentalsconsistantp(l):
        thrownoteerror('accidental note at same time as non accidental')
    if not notevaluesintegersp(l):
        thrownoteerror('not all values in note list were integers')

    for rule in specs['rules']:
        if not rule in ruletypes:
            thrownoteerror('rule ' + str(rule) + ' unknown')
        
    return Beatmap(tempo, l, specs)


def restp(t, l, specs):
    isr = False
    # handeling rests
    if (len(l) > 0) and not hasrule('norests', specs):
        # if the last note was not a rest
        if (hasrule('rests', specs) and l[-1].time + l[-1].duration >= t-0.05):
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


def random_duration(time, notelist, specs, isr, ischord):
    lv = specs['lv']
    if hasrule('shorternotes', specs):
        lv *= 6/5

    def halfp():
        offset = lv/200
        if hasrule('shorternotes', specs):
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
    if hasrule('rests', specs) and not specs['lv'] in [0,1]:
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
    if hasrule('rests', specs) and isr:
        if compare_around(time, 0):
            if not myrand(2):
                d = notelist[-1].duration
        # if off beat, good chance of the same length as the previous note
        elif myrand(5):
            d = notelist[-1].duration

    if ischord:
        # if it is a chord, big chance to simply be the same duration as the melody
        if ischord:
            if randint(0, 100) > ((lv/1.8) + 2) ** 2:
                d = notelist[-1].duration

        # also don't make it longer than the melody
        if d > notelist[-1].duration:
            d = notelist[-1].duration
            
    return d


# used to get a variation for the next round of a dance
def variation_of_notes_to_beatmap(old_notes, tempo, specs):
    newnotes = variation_of_notes(old_notes, specs)
    newb = Beatmap(tempo, newnotes, specs)
    return newb
