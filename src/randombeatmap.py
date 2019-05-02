# random_beatmap is the entrypoint- values and durations are calculated separetly

#    contracts- checked at the end of generation
# the note list in the end should be ordered early notes first
# notes added on generatively- each "layer" has the main melody note at the end of the list, chord notes inserted before it
# values should be integers

from Beatmap import Beatmap
from Note import Note
from Note import compare_around, compare_numbers_around
from notelistvariation import variation_of_notes
from notelistfunctions import *
from graphics import drawthismessage
from notelistrandomvalue import random_value
from notelistconverttodancepad import convertnotelisttodancepad

import random, copy
from random import randint
import variables, math
import devoptions


''' rule types for beatmaps that are stored in rules in the specs dictionary
A list of these rules is checked against in notelistfunctions
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
holdlongnote- hold long notes while the normal melody continues (reducing difficulty for those notes)
doublenotes- doubles all notes up two notes
combinemelodies- combine two melodies after adding them

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
        appendnotewithspecs(l, Note(rv, time, duration, True, accidentalp = accidentalp), specs)
    else:
        appendnotewithspecs(l, Note(rv, time, duration, accidentalp = accidentalp), specs)

    return (l, duration)


# returns none if not a special layer, otherwise returns a new list and duration of the layer in a tuple
def speciallayer(notelist, time, specs, specialmarkers):

    if hasrule("seperatedchordchance", specs) and not myrand(4+specs['lv']/2):
        notelist = notelist.copy()
        restdur = random_duration(time, notelist, specs, True, False)
        notedur = random_duration(time, notelist, specs, False, False)
        val1 = random_value(time+restdur, False, notelist, specs)
        
        appendnotewithspecs(notelist, Note(val1, time+restdur, notedur, False), specs)
        
        val2 = random_value(time+restdur, True, notelist, specs)

        appendnotewithspecs(notelist, Note(val2, time+restdur, notedur, True), specs)

        val3 = random_value(time+restdur, True, notelist, specs)
        
        appendnotewithspecs(notelist, Note(val3, time+restdur, notedur, True), specs)

        return (notelist, restdur+notedur)
    if hasrule("holdlongnote", specs) and not myrand(4+specs['lv']/2) and (not "holdinglongnote" in specialmarkers):
        # add a long note and then repeat until after that long note
        longnoteduration = 8
        if random.random() < 0.2 + specs['lv']/80:
            longnoteduration = 16
        accidentalp= makeaccidentalp(specs, notelist)
        if random.random() < 0.5:
            accidentalp = False

        # add the long note
        rv = random_value(time, False, notelist, specs)
        l = notelist.copy()

        # append it strait, without using special append rules
        l.append(Note(rv, time, longnoteduration, chordadditionp = True, scoremultiplier = 4+specs['lv']/2))
        
        reducedspecs = specs.copy()
        reducedspecs["lv"] = max(2, specs["lv"] - 5)
        loopresult =  looplayers(time, time+longnoteduration, l, reducedspecs, ["holdinglongnote"])
        
        return (loopresult[0], loopresult[1]-time)

    if hasrule('combinemelodies', specs) and not myrand(4+specs['lv']/2) and (not "combiningmelodies" in specialmarkers):
        # make the first time a factor of two
        timepassedin = time
        time = time + ((2-(time % 2)) % 2)
        
        # first generate a melody at 1/2 the level
        reducedspecs = specs.copy()
        reducedspecs["lv"] = max(2, int(specs["lv"] * 1 / 2))

        melodyduration = 8
        if random.random() < 0.1 + specs['lv']/80:
            melodyduration *= 2
        if random.random() < 0.05 + specs['lv']/80:
            melodyduration *= 2
        oldtime = time

        # generate the first melody
        loopresult = looplayers(time, melodyduration + time, notelist, reducedspecs, ["combiningmelodies"])
        l = loopresult[0]
        time = loopresult[1]

        firstmelody = getnoteswithintime(l, oldtime, time)
        notestocombine = copy.deepcopy(firstmelody)

        middletime = time

        # generate the second melody
        loopresult = looplayers(time, melodyduration+time, l, reducedspecs, ["combiningmelodies"])
        l = loopresult[0]
        time = loopresult[1]

        secondmelody = copy.deepcopy(getnoteswithintime(l, middletime, time))

        # make the final start time a factor of two
        finalstarttime = time + ((2-(time % 2)) % 2)

        # sync up the new notes and combine them
        for n in notestocombine:
            n.time += finalstarttime - oldtime
        for n in secondmelody:
            n.time += finalstarttime - middletime

        combined = combineaschords(secondmelody, notestocombine)
        
            
        l.extend(combined)

        time = finalstarttime + (finalstarttime - middletime)

        if devoptions.devmode:
            print("Combined melodies- oldtime: " + str(oldtime) + \
                  " melodyduration: " + str(melodyduration) + " newtime: " + str(time))
        
        return (l, time-timepassedin)
        
    return None


# returns a new list and the duration of the layer in a tuple
# valuestouse is a list of values to use instead of calling random_value, for use in repeatvaluesrepetition
def addlayer(notelist, time, specs, valuestouse = [], specialmarkers = []):
    lv = specs['lv']
    isr = restp(time, notelist, specs)

    # if there is a special layer, do that instead
    if len(valuestouse) == 0:
        sl = speciallayer(notelist, time, specs, specialmarkers)
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
    return maxtime + int(specs['lv']*3)

# loops through until maxtime, adding layers
# returns a tuple with a list of notes and the new time
def looplayers(time, maxtime, notelist, specs, specialmarkers = []):
    l = notelist.copy()
    lv = specs['lv']

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
            addl = addlayer(l, time, specs, specialmarkers=specialmarkers)
            l = addl[0]
            time += addl[1]
            
    return (l, time)
    
def random_beatmap(specs):
    # lower level for double notes rule
    if hasrule('doublenotes', specs):
        specs['lv'] = max(specs['lv'] - 6, 2)

    # higher level for beatmap mode
    if variables.settings.dancepadmodep:
        specs['lv'] = specs['lv'] + variables.dancepadlevelincrease
    
    if devoptions.devmode:
        print()
        print('output of:')
        print("   " + str(specs['rules']) + " lv: " + str(specs['lv']))
        print()

    # first update the screen to say it is being generated
    drawthismessage("generating new beatmap")
    variables.updatescreen()
    # set the variable so that time stops for a frame
    variables.generatingbeatmapp = True
    
    lv = specs['lv']
    maxtime = maxtimefromspecs(specs);
    
    

    loopresult = looplayers(0, maxtime, [], specs)
    l = loopresult[0]


    # default cheap ending- throw in a tonic at end
    lastvalue = random.choice([variables.minvalue, variables.maxvalue, 0])
    startt = round(l[-1].time + l[-1].duration + 0.5)
    appendnotewithspecs(l, Note(lastvalue, startt, randint(1,2)), specs)

    # tempo is milliseconds per beat
    tempo = (1200 * 3) / (math.sqrt(lv)*0.4+ 0.08*lv + 3.5)

    if devoptions.devmode:
        printnotelist(l)

    # then perform checks
    performnotelistchecks(l)
    
    for rule in specs['rules']:
        if not rule in ruletypes:
            thrownoteerror('rule ' + str(rule) + ' unknown')

    # now if dancepad mode change to dance pad mode
    if variables.settings.dancepadmodep:
        l = convertnotelisttodancepad(l, specs)
        performdancepadmodenotelistchecks(l)
        
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
    # now if dancepad mode change to dance pad mode
    if variables.settings.dancepadmodep:
        newnotes = convertnotelisttodancepad(newnotes, specs)
        
    newb = Beatmap(tempo, newnotes, specs)
    return newb

# repetition favors an ABAB struture of music by default


from notelistrandomvalue import random_value
import variables

import random, copy, math
from random import randint

def movednotes(old_notes, movelength):
    if len(old_notes) == 0:
        return []
    
    

    # find the max and min values
    maxval = old_notes[0].value
    minval = old_notes[0].value
    for n in old_notes:
        if n.value > maxval:
            maxval = n.value
        if n.value < minval:
            minval = n.value

    #print(str(maxval) + '  ' + str(minval) + '  ' + str(movelength))


    # give up if the range is so wide that it would be outside range if moved in either direction
    if outsiderangeq(maxval + abs(movelength)) and outsiderangeq(minval - abs(movelength)):
        return copy.deepcopy(old_notes)
    # try again if in one direction it goes off
    elif outsiderangeq(maxval + movelength) or outsiderangeq(minval + movelength):
        return movednotes(old_notes, randint(-4, 4))
    else:
        l = copy.deepcopy(old_notes)
        for n in l:
            n.newvalue(n.value + movelength)
        return l

    
# returns a dictionary with the new time and the list
# repeatduration is how long the section to repeat should be
# movelength is an offset for values of notes
# startingtime is the time the main loop left off
# maxtime is the (soft) limit on time to use
def repetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration):
    if devoptions.devmode:
        print('repetition: time: ' + str(time) + ' repeatduration: ' +
              str(repeatduration) + ' last note time: ' +
              str(listofnotes[-1].time) + ' list depth: ' +
              str(notedepth(listofnotes)) + ' skipduration: ' + str(skipduration))

    newtimeandlist = None
        
    if hasrule('repeatvalues', specs):
        newtimeandlist =  repeatvaluesrepetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration = skipduration)
    else:
        newtimeandlist = normalrepetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration = skipduration)
    if devoptions.devmode:
        print('newtime: ' + str(newtimeandlist['time']))
    return newtimeandlist

# repeat only values in order, picking new durations and times and using only the main melody values (add on chords new again)
def repeatvaluesrepetition(starttime, movelength, listofnotes, repeatduration, specs, maxtime, skipduration = 0):
    l = listofnotes.copy()

    # get the last repeatduration notes to add on again
    notestoadd = getnoteswithintime(l, starttime-repeatduration-skipduration, starttime-skipduration)
    
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

def newvaluesfornotes(listofnotes, specs):
    l = copy.deepcopy(listofnotes)
    for n in l:
        n.value = random_value(n.time, n.chordadditionp, l, specs)
    return l

# iterations is the number of times it has recursively called itself
# repeat the past layers within repeatduration, and get the layers after the number of layers specified by skipduration
def normalrepetition(time, movelength, listofnotes, repeatduration, specs, maxtime, iterations = 0, skipduration = 0):
    
    l = listofnotes.copy()

    # get the last repeatduration notes to add on again
    if not hasrule('repeatonlybeginning', specs):
        notestoadd = getnoteswithintime(l, time-repeatduration-skipduration, time-skipduration)
    else:
        notestoadd = getnoteswithintime(l, 0, repeatduration)
        
    notestoadd = copy.deepcopy(notestoadd)
    
    # with certain rules we want to call variation of notes on the list
    if hasrule('repeatvariation', specs):
        notestoadd = variation_of_notes(notestoadd, specs)

    if hasrule('repeatmove', specs):
        if devoptions.devmode and iterations == 0:
            print("movelength: " + str(movelength))
        notestoadd = movednotes(notestoadd, movelength)

    if hasrule('repeatrhythm', specs):
        notestoadd = newvaluesfornotes(notestoadd, specs)

        
    
        
    newstarttime = time
    
    if len(notestoadd) == 0:
        return {'time': newstarttime+repeatduration, 'list': l}
    
    offsetfactor = repeatduration + skipduration
    if hasrule('repeatonlybeginning', specs):
        offsetfactor = time
    
    # offset the notestoadd by the offsetfactor
    for n in notestoadd:
        n.time += offsetfactor

    newlatest = newstarttime + repeatduration
    for n in notestoadd:
        if n.time + n.duration > newlatest:
            newlatest = n.time + n.duration

    newtime = newlatest

    l.extend(notestoadd)

    # chance to repeat section again
    if newtime<maxtime and not hasrule('nodoublerepeats', specs):
        returnval = {'time': newtime, 'list': l}
        doanotherp = False

        # more likely for smaller repeatdurations
        doanotherchance = (1/2) - (repeatduration/maxtime * 0.5)
        
        # if we have already added an extra
        if iterations > 0:
            # make it so that on odd ones it is less likely
            doanotherchance = doanotherchance * (1/ ((iterations%2)*0.4 + 1.3))

        if random.random() < doanotherchance:
            doanotherp = True
                
        if doanotherp:
            newrepeatduration = getrepeatduration(l, specs, maxtime, newtime)
            returnval = normalrepetition(newtime, movelength, l, newrepeatduration, specs, maxtime, iterations+1)
        else:
            if devoptions.devmode:
                print(str(iterations+1) + " times")
        return returnval
    else:
        if devoptions.devmode:
            print(str(iterations+1) + " times")
        return {'time': newtime, 'list': l}


# assumes num % base == 0
# the log of the largest exponent of base that fits in num
def getremainderlog(num, base):
    if not num%base == 0:
        raise ValueError("getremainderlog needs num%base == 0")
    elif num<base:
        return 0

    power = base
    
    while power*base<=num:
        power *= base

    # if time is two to a power
    if power == num:
        return math.log(num, base)
    else:
        return getremainderlog(num-power, base)
    
# returns if there should be a repetition
# when time is closer to a power of two it is more likely to repeat
def repeatp(notelist, specs, ctime, maxtime):
    if len(notelist)<2:
        return False
    
    chancemultiplier = 1
    if hasrule('repeatspaceinbetween', specs):
        chancemultiplier = chancemultiplier*0.7
    elif hasrule('highrepeatchance', specs):
        chancemultiplier *= 1.3

    timerandomchance = 0
    if ctime % 2 == 0:
        timerandomchance = (1/10 + math.pow(getremainderlog(ctime, 2)/10, 0.6)*0.6)
    elif ctime % 1 == 0:
        timerandomchance = (1 / (maxtime*3))
    else:
        timerandomchance = (1/(maxtime*5))
    return random.random() < timerandomchance * chancemultiplier
        
    
# how much time to skip before grabbing notes to repeat with
def repetitiondepth(l, repeatduration, specs, maxtime, currenttime):
    
    # the possible multiples of repeatduration you can go back
    possibilities = int(currenttime/repeatduration)-1
    if possibilities <= 1:
        return 0
    else:
        # otherwise usually choose ones that are an odd repeatduration away because they tend to be the start of a phrase
        oddp = random.random()<0.85
        # how many repeatdurations back to go
        r = 0
        roffset = 0
        if oddp:
            roffset = 1
        # while it is within the possible repeatduration multiples
        while r+roffset+2<possibilities:
            if random.random()<0.3:
                r += 2
            else:
                break

        i = (r+roffset) * repeatduration
        # now a small chance it is not a multiple of repeatduration
        if random.random()<0.1 and r>0:
            # move forwards a random number
            i -= random.randint(0, repeatduration)

        return i

# returns how much of the song in time should be repeated given the current state of the list
# makes it more likely to repeat the entire thing, then cuts in half it not
def getrepeatduration(l, specs, maxtime, currenttime):
    lv = specs['lv']

    rounded = currenttime - currenttime%2

    counter = 0
    # get the biggest power of 2 that fits into remainders after powers of 2
    rlog = getremainderlog(rounded, 2)
    while rlog > 1:
        chancetobreak = 3/4
        if counter == 0:
            if hasrule("repeatspaceinbetween", specs):
                # lower the chance to repeat everything if repeatspaceinbetween
                chancetobreak *= 0.25
            
        # at each power of two a good chance to repeat that length
        if random.random() < chancetobreak:
            break
        else:
            rlog = rlog - 1
    durationwithrounded = math.pow(2, rlog)

    duration = durationwithrounded

    # cut in half if it goes over the max time too much
    if (duration + currenttime - maxtime)/maxtime > 1/4:
        duration = duration / 2
    
    # good chance to even it out by taking off the rounded bit
    if myrand(3):
        duration = duration - (currenttime - rounded)

    if duration <= 0:
        if rounded != 0:
            duration = rounded
        else:
            duration = 2
    return duration

# appends a note to a list, but takes into account rules that change this operation
def appendnotewithspecs(l, note, specs):
    # chords are inserted before other notes
    if note.chordadditionp:
        l.insert(-1, note)
    else:
        l.append(note)
        
    if hasrule('doublenotes', specs):
        # add another note two values above if it is in range and does not collide
        newval = note.value + 2
        if not outsiderangeq(newval):
            if not notecollidep(note.time, newval, note.duration, l):
                l.insert(-1, Note(newval, note.time, note.duration, chordadditionp=True, accidentalp = note.accidentalp))
        
