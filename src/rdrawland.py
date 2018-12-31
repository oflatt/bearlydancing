import pygame, variables, random, math
from pygame import draw
from random import randint
from Texture import Texture
from addtexture import addtexture
from pygame import Rect
from rdrawtree import snowclump
from rdrawrock import addlump

dirtcolor = (70, 71, 14)
pathwidth = 16

def addroad(grasssurface, leftpath, rightpath, uppath, downpath):
    surface = grasssurface
    width = surface.get_width()
    height = surface.get_height()
    randcolor = (60, 61, randint(0, 50))
    randcolor2 = (randcolor[0]-10, randcolor[1]-10, randcolor[2])
    horizontaltop = int((height/2)-(pathwidth/2))
    verticalleft = int((width/2)-(pathwidth/2))

    fillrect = None
    if leftpath and rightpath:
        fillrect = pygame.Rect(0, horizontaltop, width, pathwidth)
    elif leftpath:
        fillrect = pygame.Rect(0, horizontaltop, int((width/2)+(pathwidth/2)), pathwidth)
    elif rightpath:
        fillrect = pygame.Rect(int((width/2)-(pathwidth/2)), horizontaltop, int((width/2)+(pathwidth/2)), pathwidth)

    if fillrect != None:
        surface.fill(dirtcolor, fillrect)
        
        extendingtexture = Texture(dirtcolor, 1/25, 0.8, 0.8)
        extendingtexture.bounds = [fillrect.x, horizontaltop-3, fillrect.width, 3]
        extendingtexture.texturingbounds = [fillrect.x, horizontaltop-1, fillrect.width, 1]
        addtexture(surface, extendingtexture)

        extendingtexture = Texture(dirtcolor, 1/25, 0.8, 1/30)
        extendingtexture.bounds = [fillrect.x, horizontaltop+pathwidth, fillrect.width, 3]
        extendingtexture.texturingbounds = [fillrect.x, horizontaltop+pathwidth, fillrect.width, 1]
        addtexture(surface, extendingtexture)
    
        horizontaltexture = Texture(randcolor, 1/15, 1/3, 1/5, acceptedcolors=[dirtcolor])
        horizontaltexture2 = Texture(randcolor2, 1/20, 1/40, 1/40, acceptedcolors=[dirtcolor])
        horizontaltexture.bounds = [fillrect.x, horizontaltop-1, fillrect.width, pathwidth+2]
        horizontaltexture2.bounds = horizontaltexture.bounds
        addtexture(surface, horizontaltexture)
        addtexture(surface, horizontaltexture2)

    fillrect = None
    if uppath and downpath:
        fillrect = Rect(verticalleft, 0, pathwidth, height)
    elif uppath:
        fillrect = Rect(verticalleft, 0, pathwidth, int(height/2))
    elif downpath:
        fillrect = Rect(verticalleft, int(height/2), pathwidth, int(height/2))

    if fillrect != None:
        surface.fill(dirtcolor, fillrect)
        
        extendingtexture = Texture(dirtcolor, 1/25, 1/30, 0.8)
        extendingtexture.bounds = [verticalleft-3, fillrect.y, 3, fillrect.height]
        extendingtexture.texturingbounds = [verticalleft-1, fillrect.y, 1, fillrect.height]
        addtexture(surface, extendingtexture)
        
        extendingtexture = Texture(dirtcolor, 1/25, 1/30, 0.8)
        extendingtexture.bounds = [verticalleft+pathwidth, fillrect.y, 3, fillrect.height]
        extendingtexture.texturingbounds = [verticalleft+pathwidth, fillrect.y, 1, fillrect.height]
        addtexture(surface, extendingtexture)
        
        verticaltexture = Texture(randcolor, 1/15, 1/5, 1/3, acceptedcolors=[dirtcolor])
        verticaltexture2 = Texture(randcolor2, 1/20, 1/40, 1/40, acceptedcolors=[dirtcolor])
        verticaltexture.bounds = [verticalleft-1, fillrect.y, pathwidth+2, fillrect.height]
        verticaltexture2.bounds = verticaltexture.bounds
        addtexture(surface, verticaltexture)
        addtexture(surface, verticaltexture2)
    
    return surface

def makepatch(randomcolorsunsorted, width, height):
    def brightness(color):
        return color[0] + color[1] + color[2]
    randomcolors = sorted(randomcolorsunsorted, key=brightness)
    s = pygame.Surface([width, height], pygame.SRCALPHA)
    # randomcolors should be sorted in order of drawing, brightest is texture 3
    texture1 = Texture(randomcolors[0], 1/13, 1/10, 9/20)
    texture2 = Texture(randomcolors[1], 1/13, 1/10, 9/20)
    texture3 = Texture(randomcolors[2], 1/9, 1/10, 9/20)
    textures = [texture1, texture2, texture3]
    for t in textures:
        t.greenvarianceperspawn = 8
        t.addupq = True
        t.adddownq = False
        t.pickonedirp = True
        # skip first couple pixels
        t.texturingbounds = [0, 2, width-2, height-2]
        t.distruibution = "geometric"
        t.xinvisiblechance = 1/4
        t.yinvisiblechance = 1/4
        addtexture(s, t)
    # blue rect for seeing where pathes are
    #pygame.draw.rect(s, variables.BLUE, Rect(0,0,width,height), 1)
    return s

# currently brownchance is unused
def patchlist(patchwidth, patchheight, pinkmodeonq, brownchance = False):
    patches = []
    numofpatches = randint(5, 10)

    def randompink():
        return (randint(140, 255), randint(0, 100), randint(150, 255))
    def randombrown():
        lightness = randint(40, 65)
        return (lightness+10, lightness, lightness)
    
    randomgreens = [randint(75, 150), randint(75, 150), randint(75, 150)]
    randomgreens = sorted(randomgreens, key=int)

    
    randomcolors = []
    if pinkmodeonq:
        randomcolors = [randompink(), randompink(), randompink()]
    elif brownchance and random.random() < 0.3:
        randomcolors = [randombrown(), randombrown(), randombrown()]
    else:
        for x in range(3):
            randomcolors.append((round(randomgreens[x]/3), randomgreens[x], 8))

    for x in range(numofpatches):
        patches.append(makepatch(randomcolors, patchwidth, patchheight))
    return patches

def makegrassland(width, height, leftpath = True, rightpath = True, uppath = True, downpath = True):
    pinkmodeonq = False
    if random.random() < 0.005:
        pinkmodeonq = True
    
    patchwidth = randint(15, 30)
    patchheight = randint(15, 30)
    patches = patchlist(patchwidth, patchheight, pinkmodeonq)

    # make surface and fill it in
    surface = pygame.Surface([width, height], pygame.SRCALPHA)
    if pinkmodeonq:
        backgroundcolor = (255, 119, 228)
    else:
        backgroundcolor = (77, 112, 30)
    surface.fill(backgroundcolor)

    addpatches(surface, patches, patchwidth, patchheight)

    numblobs = random.randint(2+ int(width/height)*2, 5 + int(width/height)*2)
    for b in range(numblobs):
        blobsurface = pygame.Surface([width, height])
        bloblist = randomblob(width, height)
        pygame.draw.polygon(blobsurface, (255, 255, 255), bloblist, 0)

        patchwidth = randint(10, 25)
        patchheight = randint(10, 25)
        patches = patchlist(patchwidth, patchheight, pinkmodeonq)
        addpatches(surface, patches, patchwidth, patchheight, blobsurface)
        
        
    
    surface = addroad(surface, leftpath, rightpath, uppath, downpath)
        
    return surface

# adds the patches to the surface
# maskhitbox is a surface with a black area for where not to fill
def addpatches(surface, patches, patchwidth, patchheight, maskhitbox = None):
    # now add the patches to the land
    spacingvariability = round(patchwidth/4)
    def addrow(ypos):
        xpos = 0
        while xpos < surface.get_width():
            # check the mask
            blitp = False
            if maskhitbox == None:
                blitp = True
            else:
                if maskhitbox.get_at((xpos, ypos)) != (0,0,0, 255):
                    blitp = True
            
            if blitp:
                surface.blit(random.choice(patches), [xpos, ypos])
            xpos += patchwidth + randint(-spacingvariability, 0)

    ypos = 0
    while ypos < surface.get_height():
        addrow(ypos)
        ypos += patchheight + randint(-spacingvariability, -int(spacingvariability/3))



def makesnowland(width, height, grasstosnowp = False):
    surface = None
    if grasstosnowp:
        surface = makegrassland(width, height, uppath = False, downpath = False)
        for x in range(20):
            surface.fill((variables.snowcolor[0]-(20-x),variables.snowcolor[0]-(20-x),variables.snowcolor[0]-(20-x)), Rect(width/4 - 1 - x,0, 1, height))
        surface.fill(variables.snowcolor, Rect(0, 0, width/4-20, height))
        # now make darker pertrusion into grass
        pertrusionx = 10
        for yp in range(height):
            for xp in range(pertrusionx):
                surface.set_at((int(width/4+xp), yp), (variables.snowcolor[0]-20-xp*2, variables.snowcolor[0]-20-xp*2, variables.snowcolor[0]-20-xp*2))
            pertrusionx += randint(-2, 2)
            if pertrusionx < 1:
                pertrusionx = 1
            if pertrusionx > 20:
                pertrusionx = 20
    else:
        surface = pygame.Surface([width, height], pygame.SRCALPHA)
        surface.fill(variables.snowcolor)

    currentcolorincrease = 5
    
    def makehill(hillx, hilly, hillradiusin):
        shadowdir = random.uniform(0, math.pi*2)
        shadowrmin = random.uniform(math.pi/5, math.pi*2/3)/2
        shadowrmax = shadowrmin*random.uniform(1.6, 2.2)
        
        hillradius = hillradiusin
        currentshade = variables.snowcolor[0]
        sharpness = currentcolorincrease * random.uniform(1.5, 2)/hillradius
        while hillradius > 0:
            shadowr = shadowrmin + (shadowrmax-shadowrmin)*(hillradius/hillradiusin)
            circlethreshold(surface, hillx, hilly, hillradius, (currentshade, currentshade, currentshade), shadowdir, shadowr)
            hillradius -= 1
            if currentshade < variables.snowcolor[0]+currentcolorincrease:
                currentshade += sharpness

    for x in range(randint(3, 7)):
        hillx = randint(0, width)
        hilly = randint(0, height)
        hillr = randint(int(width/20), int(width/3))
        if not grasstosnowp or (grasstosnowp and hillx+hillr>width/4 + 25):
            snowclump(surface, hillx, hilly, groundp = True)
            snowclump(surface, randint(int(width/4 + 25), width), randint(0, height), groundp = True)
            snowclump(surface, randint(int(width/4 + 25), int(width/2)), randint(0, height), groundp = True)
            snowclump(surface, randint(int(width/4 + 25), int(width/2)), randint(0, height), groundp = True)
        else:
            makehill(hillx, hilly, hillr)
        if randint(0, int(currentcolorincrease)) <3:
            currentcolorincrease += random.uniform(2, 15)
            if currentcolorincrease > 35:
                currentcolorincrease = 35

    return surface

def circlethreshold(surface, x, y, radius, color, shadowdir, shadowr):
    steps = math.pi * radius * 2.5
    currentstep = 0
    differencec = color[0] - variables.snowcolor[0]
    
    while currentstep<=steps:
        colortouse = color
        
        angle = currentstep*2*math.pi/steps
        anglediff = abs(angle-shadowdir)
        if anglediff > math.pi:
            anglediff = math.pi*2-anglediff
        if shadowdir != None:
            if anglediff <= shadowr:
                colordarkened = color[0]-(1 - anglediff/shadowr)*differencec
                colortouse = (colordarkened, colordarkened, colordarkened)
        
        fillx = int(math.cos(angle)*radius)+x
        filly = int(math.sin(angle)*radius)+y
        if fillx >= 0 and fillx < surface.get_width() and filly>=0 and filly<surface.get_height():
            currentcolor = surface.get_at((fillx, filly))
            if colortouse[0] > currentcolor[0]:
                surface.set_at((fillx, filly), colortouse)
                    
        currentstep += 1

# given a width and a height, make a random polygon in the space
# returns a list of lists [x, y]
def randomblob(swidth, sheight):
    initialradius = random.randint(int(sheight/20), int(sheight/6))
    pointlist = []
    numofpoints = 80
    for t in range(numofpoints):
        radians = (t/numofpoints) * 2 * math.pi
        xpos = initialradius * math.cos(radians)
        ypos = initialradius * math.sin(radians)
        pointlist.append([xpos, ypos])

    # add some lumps
    numoflumps = random.randint(4, 8)
    for l in range(numoflumps):
        startpoint = random.randint(0, numofpoints)
        addlump(pointlist, startpoint,
                startpoint+random.randint(int(numofpoints/4), int(numofpoints/2)),
                initialradius*random.uniform(-0.5, 2),
                random.choice([True, False]))
        
    center = (random.randint(0, swidth), random.randint(0, sheight))
    for p in pointlist:
        p[0] += center[0]
        p[1] += center[1]

    return pointlist
