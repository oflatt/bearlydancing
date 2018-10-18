import variables
from notelistrandomvalue import random_value
from notelistfunctions import *

import random, copy
from random import randint



# future work: add the addition of chords to variation of notes
def variation_of_notes(old_notes, specs):
    # print('called variation of notes, old notes:')
    # printnotelist(old_notes)
    # print('end of old notes')

    #def random_inrange():
    #    return randint(variables.minvalue, variables.maxvalue)

    l = copy.deepcopy(old_notes)
    basereplacechance = 1/6
    replacechancelastnotefactor = 1

    for p in range(len(l)):
        replacechancefurtherfactorslope = 1.5/len(l)
        # make it so that notes later in the list of notes to vary have a higher chance of changing
        replacechancefurtherfactor = 1 + replacechancefurtherfactorslope*p
        
        # sometimes change the value of the note, if the new value does not cause it to overlap any existing notes
        if random.random() < basereplacechance*replacechancefurtherfactor*replacechancelastnotefactor:
            oldnote = l[p]
            # get a new value based on the existing notes
            newvalue = random_value(oldnote.time, oldnote.chordadditionp, l[0:p], specs)

            iscopy = False
            c = 0

            # check if the new value would cause it to overlap another note
            potentialreplace = copy.copy(oldnote)
            potentialreplace.newvalue(newvalue)
            iscopy = notecollidebesidesselfp(potentialreplace, l)
                
            if not iscopy:
                l[p].newvalue(newvalue)
                # make the chance to replace the next note higher
                replacechancelastnotefactor = 2
            else:
                replacechancelastnotefactor = 1
        else:
            replacechancelastnotefactor = 1

    return (l)

