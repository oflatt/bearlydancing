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

    def random_inrange():
        return randint(variables.minvalue, variables.maxvalue)

    l = copy.deepcopy(old_notes)
    replacechance = 1.0/5.0

    for p in range(len(l)):
        # sometimes change the value of the note, if the new value does not cause it to overlap any existing notes
        if random.random() < replacechance:
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
                replacechance = 1.0/3.0
            else:
                replacechance = 1.0/5.0
        else:
            replacechance = 1.0/5.0

    return (l)

