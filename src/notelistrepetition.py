# repetition favors an ABAB struture of music by default

from notelistfunctions import *
from notelistvariation import variation_of_notes
from notelistrandomvalue import random_value
import variables

import random, copy, math
from random import randint

def movednotes(old_notes, movelength):
    if len(old_notes) == 0:
        return []
    
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

# returns a dictionary with the new time and the list
# repeatduration is how long the section to repeat should be
# movelength is an offset for values of notes
# startingtime is the time the main loop left off
# maxtime is the (soft) limit on time to use
def repetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration):
    if variables.devmode:
        print('repetition: time: ' + str(time) + ' repeatduration: ' +
              str(repeatduration) + ' last note time: ' +
              str(listofnotes[-1].time) + ' list depth: ' +
              str(notedepth(listofnotes)) + ' skipduration: ' + str(skipduration))

    newtimeandlist = None
        
    if hasrule('repeatvalues', specs):
        newtimeandlist =  repeatvaluesrepetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration = skipduration)
    else:
        newtimeandlist = normalrepetition(time, movelength, listofnotes, repeatduration, specs, maxtime, skipduration = skipduration)
    if variables.devmode:
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
        if variables.devmode and iterations == 0:
            print("movelength: " + str(movelength))
        notestoadd = movednotes(notestoadd, movelength)

    if hasrule('repeatrhythm', specs):
        notestoadd = newvaluesfornotes(notestoadd, specs)

    oldendtime = time
    if hasrule('repeatonlybeginning', specs):
        oldendtime = notestoadd[-1].time + notestoadd[-1].duration
        
    newstarttime = time
    
    if len(notestoadd) == 0:
        return {'time': newstarttime+repeatduration, 'list': l}
    
    offsetfactor = repeatduration + skipduration

    
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
            if variables.devmode:
                print(str(iterations+1) + " times")
        return returnval
    else:
        if variables.devmode:
            print(str(iterations+1) + " times")
        return {'time': newtime, 'list': l}


# assumes num % base == 0
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
# when time is closer to a power of two it is more likely to repeat TODO
def repeatp(notelist, specs, ctime, maxtime):
    if len(notelist)<2:
        return False
    
    chancemultiplier = 1
    if hasrule('repeatspaceinbetween', specs):
        chancemultiplier = chancemultiplier*0.75
    elif hasrule('highrepeatchance', specs):
        chancemultiplier *= 1.3
    
    if ctime % 2 == 0:
        return random.random() < (1/6 + math.sqrt(getremainderlog(ctime, 2))/10) * chancemultiplier
    elif ctime % 1 == 0:
        return random.random() < (1 / (maxtime*3)) * chancemultiplier
    else:
        return random.random() < (1/(maxtime*5))*chancemultiplier
        
    
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
    return duration
