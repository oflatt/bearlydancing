# repetition favors an ABAB struture of music by default

from notelistfunctions import *
from notelistvariation import variation_of_notes
from notelistrandomvalue import random_value
import variables

import random, copy
from random import randint

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

# returns a dictionary with the new time and the list
# repeatlength is the number of notes to repeat
# movelength is an offset for values of notes
# startingtime is the time the main loop left off
# maxtime is the (soft) limit on time to use
def repetition(time, movelength, listofnotes, repeatlength, specs, maxtime, skiplayers):
    if variables.devmode:
        print('repetition: time: ' + str(time) + ' repeatlength: ' +
              str(repeatlength) + ' last note time: ' + str(listofnotes[-1].time) + ' depth: ' + str(notedepth(listofnotes)))
        
    if 'repeatvalues' in specs['rules']:
        return repeatvaluesrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime, skiplayers = skiplayers)
    else:
        return normalrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime, skiplayers = skiplayers)


# repeat only values in order, picking new durations and times and using only the main melody values (add on chords new again)
def repeatvaluesrepetition(starttime, movelength, listofnotes, repeatlength, specs, maxtime, skiplayers = 0):
    l = listofnotes.copy()

    # get the last repeatlength notes to add on again
    notestoadd = getlastnlayers(l, repeatlength, skiplayers = skiplayers)
    
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
# repeat the past repeatlength layers, and get the layers after the number of layers specified by skiplayers
def normalrepetition(time, movelength, listofnotes, repeatlength, specs, maxtime, iterations = 0, skiplayers = 0):
    l = listofnotes.copy()

    # get the last repeatlength notes to add on again
    if not 'repeatonlybeginning' in specs['rules']:
        notestoadd = getlastnlayers(l, repeatlength, skiplayers = skiplayers)
    else:
        notestoadd = getfirstnlayers(l, repeatlength)
        
    notestoadd = copy.deepcopy(notestoadd)
        
    
    # with certain rules we want to call variation of notes on the list
    if 'repeatvariation' in specs['rules']:
        notestoadd = variation_of_notes(notestoadd, specs)

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

    # chance to repeat section again
    if newtime<maxtime and not 'nodoublerepeats' in specs['rules']:
        returnval = {'time': newtime, 'list': l}
        doanotherp = False

        # more likely for smaller repeatlengths
        doanotherchance = (2/3) - (repeatlength/len(l) * 0.5)
        
        # if we have already added an extra
        if iterations > 0:
            # make it so that on odd ones it is less likely
            doanotherchance = doanotherchance * (1/ ((iterations%2)*0.4 + 1.3))

        if random.random() < doanotherchance:
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

# how many layers to skip before grabbing notes to repeat with
def repetitiondepth(l, repeatlength, specs, maxtime):
    numoflayers = notedepth(l)
    # the possible multiples of repeatlength you can go back
    possibilities = int(numoflayers/repeatlength)-1
    if possibilities <= 1:
        return 0
    else:
        # otherwise usually choose ones that are an odd repeatlength away because they tend to be the start of a phrase
        oddp = random.random()<0.85
        # how many repeatlengths back to go
        r = 0
        roffset = 0
        if oddp:
            roffset = 1
        # while it is within the possible repeatlength multiples
        while r+roffset+2<possibilities:
            if random.random()<0.2:
                r += 2

        i = r * repeatlength
        # now a small chance it is not a multiple of repeatlength
        if random.random()<0.1 and r>0:
            # move forwards a random number
            i -= random.randint(0, repeatlength)

        return i

# TODO: make repeatlength based on powers of two with current list
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

        # make even repeatlengths more likely
        if rlength%2 == 1:
            if myrand(1):
                rlength += 1
        return rlength
