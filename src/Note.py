import pygame


import variables
from FrozenClass import FrozenClass
from graphics import getTextPic


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

    def __init__(self, value, time, duration, chordadditionp = False, accidentalp = False, scoremultiplier = 1):
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

        # multiplies the score that you get from that note
        self.scoremultiplier = int(scoremultiplier)

        # screen value is changed for dance pad mode
        self.screenvalue = Note.value_to_screenvalue(self.value)
        
        self._freeze()

    def equalp(self, othernote):
        return self.time == othernote.time and \
            self.duration == othernote.duration and \
            self.value == othernote.value and \
            self.accidentalp == othernote.accidentalp and \
            self.chordadditionp == othernote.chordadditionp and \
            self.scoremultiplier == othernote.scoremultiplier

    def getscreenvalue(self):
        return self.screenvalue

    @staticmethod
    def value_to_screenvalue(v):
        sv = v % 7
        if (sv == 0 and v >= 7):
            sv = 7
        elif (sv < 0):
            sv += 7
        return sv

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
        borderwidth = 0 # zero signals pygame to draw it filled in
        

        # subtract height to y because the pos is the bottom of the rectangle
        if self.ison:
            color = variables.notes_colors[self.screenvalue]
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
        middleofnoteoffset = 0

        if self.scoremultiplier != 1:
            borderwidth = int(end_height/2)
            middleofnoteoffset = int((width-int(width*0.7))/2)
            width = int(width * 0.7)
            
        
        def drawend(x, y, color, endshape):
            if endshape == "square":
                pygame.draw.rect(variables.screen, color,
                                 [x, y, endwidth, end_height], borderwidth)
            elif endshape == "triangle":
                fourthx = endwidth/4
                centery = y + end_height/2
                pygame.draw.polygon(variables.screen, color,
                                    [[x, centery], [x+fourthx, y], [x+3*fourthx, y],
                                     [x+endwidth, centery], [x+3*fourthx, y+end_height], [x+fourthx, y+end_height]], borderwidth)
            elif endshape == "round":
                pygame.draw.ellipse(variables.screen, color,
                                    [x, y, endwidth, end_height], borderwidth)

        def drawmid(y, mheight, color):
            x = p[0] + middleofnoteoffset
            if mheight > 0:
                if self.shape() == "square":
                    pygame.draw.rect(variables.screen, color, [x, y, width, mheight], borderwidth)
                elif self.shape() == "triangle":
                    fourthx = width/4
                    pygame.draw.polygon(variables.screen, color,
                                        [[x+3*fourthx, y], [x+fourthx, y], [x, y + mheight/2],
                                         [x+fourthx, y+mheight], [x+3*fourthx, y+mheight], [x+width, y + mheight/2]],
                                        borderwidth)
                elif self.shape() == "round":
                    ellipsesurface = pygame.Surface((width, mheight), pygame.SRCALPHA)
                    pygame.draw.ellipse(ellipsesurface, color,
                                        [0, -20, width, mheight+40],
                                        borderwidth)
                    variables.screen.blit(ellipsesurface, [x, y])

                # draw the multiplier if it is not 1
                if self.scoremultiplier != 1:
                    scorepic = getTextPic("x" + str(self.scoremultiplier), variables.gettextsize(), variables.WHITE)
                    variables.screen.blit(scorepic, (x, y + mheight/2 - variables.gettextsize()/2))
                    
                # now draw pink line if it is an accidental
                if self.accidentalp:
                    pygame.draw.rect(variables.screen, variables.PINK, [x+width/4, y, width/2, mheight]) # don't change border width
                

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

        # don't draw it if it has been played
