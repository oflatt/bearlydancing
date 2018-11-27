import variables
from notelistfunctions import *

import random, copy, math
from random import randint

def centerwithspecs(lowerbound, upperbound, specs):
    crange = (lowerbound - upperbound)
    center = lowerbound + crange/2

    if hasrule("highervalues", specs):
        center += crange/3
    elif hasrule("lowervalues", specs):
        center -= crange/3
    return center

def randtrianglevalwithspecs(lowerbound, upperbound, specs, defaulttrianglep = False):
    center = centerwithspecs(lowerbound, upperbound, specs)
        
    return int(round(random.triangular(lowerbound, upperbound, center)))

def random_value(t, ischord, unflippedlist, specs):
    # flip l because it's easier to look at it that way
    l = unflippedlist[::-1]

    rv = randtrianglevalwithspecs(variables.minvalue, variables.maxvalue, specs)
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

# picks a sign for the moveby value based upon if highervalues or lowervalues is in the rules of the specs
def movebywithspecs(currentv, moveby, specs):
    center = centerwithspecs(variables.minvalue, variables.maxvalue, specs)
    # bias towards the center
    offby = abs(currentv - center) / (variables.maxvalue - variables.minvalue)
    towardssign = center - currentv
    moveby = abs(moveby)
    strengthofbias = 0.6
    if random.random() > 0.5-offby*strengthofbias:
        return int(currentv + math.copysign(moveby, towardssign))
    else:
        return int(currentv + math.copysign(moveby, -towardssign))
    
# assume depth>0
def melodic_value(rv, depth, specs, l):
    value = None
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
                value = movebywithspecs(rv, 2, specs)
        else:
            value = movebywithspecs(rv, 2, specs)

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
                value = movebywithspecs(rv, rd, specs)
        else:
            # near previous note
            rd = randint(1, 2)
            value = movebywithspecs(rv, rd, specs)

    #1/3 chance to be within 6
    elif not myrand(2):
        rd = randint(1, 6)
        value = movebywithspecs(rv, rd, specs)
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
        # jump in opposite direction
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
                return movebywithspecs(startingpoint, distance_away, specs)
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
                    value = movebywithspecs(secondv, 1, specs)
                # otherwise within 2
                else:
                    value = movebywithspecs(secondv, random.choice([1, 2]), specs)
        else:
            value = not_alternating()
    else:
        value = not_alternating()

    if outsiderangeq(value):
        return alternating_value(rv, depth, specs, l)
    else:
        return value
