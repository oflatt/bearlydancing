import random, copy

from Note import compare_numbers_around
from Note import Note

dancepadtable = {0:(True,False,False,False), 1:(False,True,False,False),
                 2:(False,False,True,False), 3:(False,False,False,True),
                 4:(True,True,False,False), 5:(True,False,True,False),
                 6:(True,False,False,True), 7:(False,True,True,False),
                 8:(False,True,False,True), 9:(False,False,True,True)}

# collisions are simpler for dancepad mode because all notes are only points
def dancepadnotecollidesp(notelist, noteval, notetime):
    i = len(notelist) - 1
    n = None
    while i > 0:
        n = notelist[i]
        if compare_numbers_around(notetime, n.time, within = 0.01) and noteval == n.value:
            return True
        elif n.time < notetime:
            break
        
        i += -1

    return False

# returns a tuple with true for which arrows are part of the value
# the tuple corresponds to (left, right, up, down)
def dancepadval(note, tableoffset):
    if note.accidentalp:
            return dancepadtable[(note.value+12) % 10]

    # if we return a combination one
    if note.duration < 1 and (note.value+12) % 6 == 0:
            return dancepadtable[((int((note.value+12)/6)+tableoffset) % 6) + 4]
    else:
        return dancepadtable[(note.value+12) % 4]


# builds a new list that works in dance pad mode
# maps values in notes to new notes with values 0-3
# assumes all contracts on a note list
def convertnotelisttodancepad(notelist, specs):
    l = []
    # table offset makes which combinations of arrows vary
    tableoffset = random.randint(0, 5)

    for n in notelist:
        newvallist = dancepadval(n, tableoffset)

        for i in range(4):
            if newvallist[i] and not dancepadnotecollidesp(l, i, n.time):
                newn = copy.copy(n)
                newn.duration = 1
                newn.value = i
                l.append(newn)

    return l
