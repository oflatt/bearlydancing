import pygame
import variables
from FrozenClass import FrozenClass


def value_to_screenvalue(v):
    sv = v % 7
    if (sv == 0 and v >= 7):
        sv = 7
    elif (sv < 0):
        sv += 7
    return sv

# compare_within is inclusive, and adds a little on for floating point error
def compare_around(num, comparedto, within = 0, modulus = 1):
    left = comparedto-(within + 0.000001)
    right = comparedto+(within + 0.000001)
    if left<0 or right>modulus:
        return num%modulus >= left%modulus or num%modulus <= right%modulus
    else:
        return left%modulus <= num%modulus <= right%modulus

def compare_numbers_around(num, othernum, within = 0):
    return abs(num-othernum) <= 0.000001+within

# tests
if not compare_around(28.1, 0, 0.1, 1):
    print("Note: compare_around test 1 failed")
if not compare_around(28.5, 0.4, 0.2, 1):
    print("Note: compare_around test 2 failed")
    
def beatshape(time):
    if compare_around(time, 0, 0.005, 1):
        return "square"
    elif compare_around(time, 0.5, 0.005, 1):
        return "triangle"
    else:
        return "round"

class Note(FrozenClass):

    def __init__(self, value, time, duration, chordadditionp = False, accidentalp = False):
        # value is the placement in the current scale (instrument) that the note is, 0 is the first note, can go neg
        self.value = value
        
        # time is the value in number of beats from beginning
        self.time = time
        self.duration = duration
        
        self.pos = [0,0]
        # if they miss the note or stop playing it halfway ison will turn false and they will miss the note
        self.ison = True

        self.beginning_score = None
        self.end_score = None

        # drawing
        self.height_offset = 0

        # raises the note one half step up
        self.accidentalp = accidentalp
        
        # this is for generating notes and debugging
        self.chordadditionp = chordadditionp
        self.collidedwithanotherp = False

        self._freeze()

    def screenvalue(self):
        return value_to_screenvalue(self.value)

    def shape(self):
        return beatshape(self.time)

    def secondshape(self):
        return beatshape(self.time+self.duration)
    
    def newvalue(self, newval):
        self.value = newval

    def height(self, tempo):
        return self.duration * (variables.getpadypos() / variables.settings.notes_per_screen)

    # bottom end of note included, top of note goes over height
    # detection is by the bottom of each end of the note
    def draw(self, tempo):
        # only draw if it is on screen
        if self.pos[1]>0:
            self.drawhelper(tempo)

    def drawhelper(self, tempo):
        width = variables.width / 20
        height = self.height(tempo)

        # subtract height to y because the pos is the bottom of the rectangle
        if self.ison:
            color = variables.notes_colors[self.screenvalue()]
        else:
            color = variables.GREY

        darkercolor = []
        for rgbval in color:
            if rgbval -50 < 0:
                darkercolor.append(0)
            else:
                darkercolor.append(rgbval-50)

        end_height = variables.height / 80

        p = self.pos

        topendy = p[1] - height - end_height
        endx = p[0] - width/8
        endwidth = width * 1.25

        def drawend(x, y, color, endshape):
            if endshape == "square":
                pygame.draw.rect(variables.screen, color,
                                 [x, y, endwidth, end_height])
            elif endshape == "triangle":
                fourthx = endwidth/4
                centery = y + end_height/2
                pygame.draw.polygon(variables.screen, color,
                                    [[x, centery], [x+fourthx, y], [x+3*fourthx, y],
                                     [x+endwidth, centery], [x+3*fourthx, y+end_height], [x+fourthx, y+end_height]])
            elif endshape == "round":
                pygame.draw.ellipse(variables.screen, color,
                                    [x, y, endwidth, end_height])

        def drawmid(y, mheight, color):
            if mheight > 0:
                if self.shape() == "square":
                    pygame.draw.rect(variables.screen, color, [p[0], y, width, mheight])
                elif self.shape() == "triangle":
                    fourthx = width/4
                    pygame.draw.polygon(variables.screen, color,
                                        [[p[0]+3*fourthx, y], [p[0]+fourthx, y], [p[0], y + mheight/2],
                                         [p[0]+fourthx, y+mheight], [p[0]+3*fourthx, y+mheight], [p[0]+width, y + mheight/2]])
                elif self.shape() == "round":
                    ellipsesurface = pygame.Surface((width, mheight), pygame.SRCALPHA)
                    pygame.draw.ellipse(ellipsesurface, color,
                                        [0, -20, width, mheight+40])
                    variables.screen.blit(ellipsesurface, [p[0], y])

                # now draw pink line if it is an accidental
                if self.accidentalp:
                    pygame.draw.rect(variables.screen, variables.PINK, [p[0]+width/4, y, width/2, mheight])
                

        # subtract height from y because the pos is the bottom of the rectangle
        # the first case is if the note is currently being played
        if self.ison and variables.getpadypos() > p[1] - height and self.beginning_score != None and self.end_score == None:
            mheight = height+1 - (p[1]-variables.getpadypos())
            drawmid(p[1]-height-1, mheight, darkercolor)
            drawend(endx, topendy, color, self.secondshape())
            variables.dirtyrects.append(pygame.Rect(endx, topendy-10, endwidth, mheight+end_height*20))

        # second case is if the note was interrupted in the middle and counted as a miss
        elif not self.height_offset == 0:
            if (height - self.height_offset > 1):
                drawmid(p[1]-height-1, height+1-self.height_offset, darkercolor)
                drawend(endx, topendy, color, self.secondshape())
            variables.dirtyrects.append(pygame.Rect(endx, topendy-10, endwidth, height+end_height+1+self.height_offset+20))

        # third case is if it has either been missed or has not been played yet (normal draw)
        elif self.beginning_score == None or self.beginning_score == variables.miss_value or self.end_score == variables.miss_value:
            #middle of note
            drawmid(p[1]-height-1, height+2-end_height, darkercolor)
            #top
            drawend(endx, topendy, color, self.secondshape())
            #bottom of note
            drawend(endx, p[1]-end_height, color, self.shape())
            variables.dirtyrects.append(pygame.Rect(endx, topendy-10, endwidth, height+end_height+2+20))

        #don't draw it if it has been played
