import variables, classvar, enemies, graphics, pygame, copy
import Map
from conversations import getconversation
from Animation import Animation
from graphics import scale_pure
from graphics import GR
from Rock import Rock
from Exit import Exit
from pygame import Rect
from Conversation import Conversation
from Speak import Speak
from variables import displayscale
from EventRequirement import EventRequirement
from random import randint
from mapsvars import *





housewidth = GR["honeyhouseoutside"]["w"]
househeight = GR["honeyhouseoutside"]["h"]
houserock = Rock("honeyhouseoutside", housewidth, 0,
                 [0,1/2,1,1/2 - (20/GR["honeyhouseoutside"]["img"].get_height())]) # type: ignore

# honeyhome#####################################################################################
insidewidth = GR["honeyhouseinside"]["w"]
insideheight = GR["honeyhouseinside"]["h"]
table = Rock("table", 75, 110, None)
table.background_range = Rect(0, 110 + int(table.h / 2), 9999999, 9999999)
littleletter = Rock('letter', 75, 110, None)
littleletter.background_range = table.background_range.copy()

bed = Rock(["honeywakesup0", "honeywakesup1", "honeywakesup2", "honeywakesup3", "bed"],
           8, 38, None, name = "bed")


bed.background_range = pygame.Rect(0,0,9999999,9999999)
stashlist = []
for x in range(10):
    stashname = "stash0" + str(x)
    stashlist.append(stashname)
    
honeyhome = Map.Map("honeyhouseinside",
                [bed,
                 table,
                 littleletter,
                 Rock(stashlist, 131, 55, [0, 0.9, 1, 0.1], name="stash")],
                shadowsp = False)

eatfromstash = Conversation("eatfromstash",
                            [],
                            speaksafter = [[],[],[],[],[],[],[],[],
                                           [getconversation("hungryspeak")]],
                            switchtheserocks="stash")

eatfromstashoffset = 10
eatfromstash.area = [131+eatfromstashoffset, 61, GR["stash00"]["w"]-2*eatfromstashoffset, GR["stash00"]["h"]]

doorexit = Exit([35 + honeyw / 2, 165, 37 - honeyw, extraarea],
                True, 'outside1',
                GR["honeyhouseoutside"]["w"] * 0.3 + houserock.x, GR["honeyhouseoutside"]["h"] - honeyh + honeyfeetheight-20*p)
doorexit.eventrequirements = [EventRequirement("letter")]

blockexit = getconversation("hungry")
blockexit.area = doorexit.area
blockexit.eventrequirements = [EventRequirement("letter", -1, 1)]

honeyhome.conversations = [eatfromstash, blockexit]

honeyhome.startpoint = [28, 39]

letterexit = Exit([67, 100, 20, 30],
                  True, 'letter',
                  GR["paper"]['w']*(3/10), 0)
letterexit.storyevent = "letter"

honeyhome.exitareas = [doorexit,
                       letterexit]
honeyhome.colliderects = [Rect(0, 0, 30, 74),  # bed
                          Rect(0, 0, insidewidth, 48),  # wall
                          Rect(44, 0, 26, 60),  # wardrobe
                          Rect(75, 110 + 11, 44, 13)]  # table
honeyhome.uselastposq = True


# letter########################################################################################
paperscale = int((GR["honeyhouseinside"]["h"]/GR["paper"]["h"])+1) # so it is as big as inside to put the text in it

GR["backgroundforpaper"]["img"] = variables.transformscale(GR["backgroundforpaper"]["img"],
                                                         [GR["backgroundforpaper"]["w"]*paperscale,
                                                          GR["backgroundforpaper"]["h"]*paperscale])
                                                          
GR["backgroundforpaper"]["w"] *= paperscale
GR["backgroundforpaper"]["h"] *= paperscale
b = GR['backgroundforpaper']['w'] / 10

GR["paper"]["img"] = variables.transformscale(GR["paper"]["img"],
                                            [GR["paper"]["w"]*paperscale,
                                             GR["paper"]["h"]*paperscale])
GR["paper"]["w"] *= paperscale
GR["paper"]["h"] *= paperscale
bigpaper = Rock("paper", (GR["backgroundforpaper"]['w'] - GR["paper"]["w"]) / 2, 0, None)
bigpaper.background_range = None  # always in front
s1 = variables.font.render("I stole your lunch.", 0, variables.BLACK).convert()
s2 = variables.font.render("-Trash Panda", 0, variables.BLACK).convert()
lettertextscalefactor = (GR["paper"]['w'] * (3/4)) / s1.get_width()
s1 = variables.transformscale(s1, [int(lettertextscalefactor*s1.get_width()), int(lettertextscalefactor*s1.get_height())])
s2 = variables.transformscale(s2, [int(lettertextscalefactor*s2.get_width()), int(lettertextscalefactor*s2.get_height())])
graphics.addsurfaceGR(s1, "stolelunchtext", [s1.get_width(), s1.get_height()])
graphics.addsurfaceGR(s2, "tplunchtext", [s2.get_width(), s2.get_height()])

w1 = Rock("stolelunchtext", b * 5 - s1.get_width() / 2, b * 3, None)
w1.background_range = None
w2 = Rock("tplunchtext", b * 5 - s2.get_width() / 2, b * 4.5, None)
w2.background_range = None

letter = Map.Map("backgroundforpaper", [bigpaper,
                                        w1,
                                        w2],
             shadowsp = False)

letter.playerenabledp = False

thatr = getconversation("thatracoon")
thatr.area = [-b*10, -b*10, b * 30, b * 30]
thatr.storyevent = "that racoon"
thatr.eventrequirements = [EventRequirement("that racoon", -1, 1)]

letter.conversations = [thatr]
letter.exitareas = [Exit([0, 0, b * 10, b * 10], True, 'honeyhome', 'same', 'same')]


# outside1######################################################################################
b = GR["horizontal"]["w"] / 10

#stands for random pine tree
rpt = graphics.pinetree()
outsidewidth = 900
outsideheight = 500

rgrassland = graphics.grassland(outsidewidth, outsideheight)
treerock = Rock(rpt, 3.5 * b + housewidth, 1.5 * b, treecollidesection)
meangreeny = treerock.y + GR[rpt]["h"] - GR["meangreen0"]["h"]
meangreenrock = Rock("meangreen0", treerock.x + 0.5 * b, meangreeny, [0, 0.81, 1, 0.19])

cleararearect = Rect(houserock.x, houserock.y, 500-houserock.x, treerock.y+treerock.h-houserock.y)

chimneyrock = Rock([Animation(["flyingchimney0"], 1),
                    Animation(["flyingchimney1", "flyingchimney2", "flyingchimney3"], 20),
                    enemies.chimneyanimation], houserock.x+ 136-25, houserock.y+ 64-43, None, "chimney")

secretchimneyactivation = Conversation("secretchimneyactivation",[])
secretchimneyactivation.area = [houserock.x + houserock.w/2 - 5, houserock.y + houserock.h/2 - 2, 4, houserock.h/10]
secretchimneyactivation.switchtheserocks = ["chimney"]
secretchimneyactivation.storyevent = "chimneyactivation"
secretchimneyactivation.eventrequirements = [EventRequirement("chimneyactivation", -1, 1)]

chimneybattlec = getconversation("chimneytalk")
chimneybattlec.area = [450+chimneyrock.w/3, 190, chimneyrock.w/3, 20]
chimneybattlec.eventrequirements = [EventRequirement("chimneyactivation")]
chimneye = copy.copy(enemies.enemies["chimney"])
chimneye.lv = 7
chimneybattlec.special_battle = chimneye

beatchimneyc = getconversation("beatchimneyc")
makeconversationreward(beatchimneyc, chimneybattlec.special_battle, "chromatic")

outside1 = Map.Map(rgrassland,
               [houserock,
                Rock(graphics.greyrock(), 6.5 * b, 7.5 * b, variables.ROCKCOLLIDESECTION),
                treerock,
                meangreenrock,
                chimneyrock])

outside1.populate_with("pinetree", 4, [cleararearect])
outside1.populate_with("flower", randint(3, 7), [cleararearect])


outside1.startpoint = [b * 8, b * 4]
outside1.exitareas = [Exit("right", False, 'outside2', "left", "same"),
                      Exit("left", False, 'jeremyhome', "right",
                           "same"),
                      Exit([housewidth * (1.5 / 5) + houserock.x, househeight * (3 / 5), housewidth * (1 / 10),
                            househeight * (1 / 5)],
                           True, 'honeyhome',
                           41, insideheight - honeyh)]

outside1.lvrange = [1, 2]
outside1c = getconversation("meaniestops")
outside1c.area = [treerock.x, 0, outsidewidth, outsideheight]
outside1c.isbutton = False
outside1c.eventrequirements = [EventRequirement("beat meanie", -1, 1)]

outside1c.special_battle = copy.copy(enemies.enemies["mean green"])
# lv of 0 triggers tutorial
outside1c.special_battle.lv = 0
outside1c.special_battle.storyeventsonwin = ["beat meanie"]
outside1c.special_battle.storyeventsonflee = ["beat meanie", "flee from meanie"]

goodc = getconversation("prettygood")
goodc.area = [0,0,outsidewidth,outsideheight]
goodc.storyevent = "goodc"
goodc.eventrequirements = [EventRequirement("beat meanie"), EventRequirement("goodc", -1, 1),
                           EventRequirement("flee from meanie", -1, 1)]
goodc.isbutton = False

gotoforest = getconversation("gotoforest")
gotoforest.area = [0,0,b/2,b*20]
gotoforest.isbutton = False
gotoforest.exitteleport = [b/2 + honeyw/4, "same"]
gotoforest.eventrequirements = [EventRequirement("beat meanie", -1, 1)]

want2go = getconversation("want2go")
want2go.area = [meangreenrock.x - 5, meangreenrock.y - 5, meangreenrock.w+10, meangreenrock.h+10]
want2gospeak = want2go.speaks[0]
want2gospeak.special_battle = copy.copy(enemies.enemies["mean green"])
want2gospeak.special_battle.lv = 1
want2go.eventrequirements = [EventRequirement("beat meanie")]

outside1.conversations = [outside1c, gotoforest, goodc, want2go, secretchimneyactivation,
                          chimneybattlec, getconversation("letsflee"), getconversation("losetochimney"),
                          beatchimneyc]

outside1.colliderects = [Rect(houserock.x-3, houserock.y+houserock.collidesection[1], 3, houserock.collidesection[3])]
