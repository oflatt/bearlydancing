#!/usr/bin/python

import variables, pygame
from Conversation import Conversation
from copy import deepcopy
from Speak import Speak

# not used anymore- handled by the name menu
#outofbed = Conversation("outofbed", [], speaksafter = [[],[],[]], switchtheserocks = "bed")

everyyears = Speak("honeyside0", ["I'm sleepy.",
                                      "I'm more hungry than sleepy. Let's go get my lunch back from TP."])
everyyears.side = 'l'

hungry = Conversation("hungry",[Speak("honeyside0", ["I'm hungry...",
                                            "And I have no reason to go outside.",
                                            "Quick lunch, and back to sleep.",
                                            "I'll eat the quiche I made yesterday."])])

hungryspeak = Speak("honeyside0",["And... I'm still hungry"])

thatracoon = Conversation("thatracoon", [Speak("honeyside0", ["That raccoon...",
                                                "I knew he was up to no good yesterday.",
                                                "Now I have to track him down."]),
                           everyyears])

honeydotspeak = Speak("honeyside3", ["..."])

monster = ["Greenie Meanie: Who goes there!"]
ohhoney4 = ["I'm looking for TP."]
monster2 = ["No one may pass!"]
ohhoney5 = ["You want to fight?"]
monster3 = ["No no, that would be stupid.", "We'll settle this with a DANCE-OFF!"]
ohhoney8 = ["...",
            "Hey, User.",
            "You be the bard and play the music.",
            "I'll handle the dancing myself."]

jeremy = Conversation("jeremy",[Speak("jeremy0", ["Howdey, Honey",
                                         "Have a random piece of advice.",
                                         "Better dancers live further away from your home for whatever reason.",
                                         "If you don't feel ready to continue, just stick around in one area for a while."])],
                      [Speak("jeremy0", ["I already told you, walk around and practice before continuing.",
                                         "You can't face me yet."]),
                       Speak("jeremy0", ["Bug off."])])

jeremyaftersteve = Conversation("jeremyaftersteve",
                                [Speak("jeremy0", ["Ah, so you beat Steve."]),
                                 Speak("jeremy0", ["Me? You are not ready to face me."], side = "left")],
                                [Speak("jeremy0", ["You aren't ready to face me."])])

meaniestops = Conversation("meaniestops",
                           [Speak("meangreen0", monster),
                            Speak("honeyside3", ohhoney4),
                            Speak("meangreen0", monster2),
                            Speak("honeyside3", ohhoney5),
                            Speak("meangreen0", monster3),
                            Speak("honeyback3", ohhoney8, side="right")],
                           [Speak("honeyback3", ["Here we go again..."])])

dancelionpass = Conversation("dancelionpass",
                             [Speak("dancelion0",
                                    ["Hey, I'll only let you through if you beat me in a dance battle."]),
                              honeydotspeak,
                              Speak("dancelion0",
                                    ["Wait, you telling me your bard can't play in the key of C minor?",
                                     "Come back when they can."])],
                             [Speak("dancelion0", ["Come back when your bard can play in the key of C minor.",
                                                       "I only dance to music in that key."])])

dancelionbattle = Conversation("dancelion",
                               [Speak("dancelion0",
                                      ["I am dance lion and I love the key of C minor.",
                                       "Hit it."])])

gotoforest = Conversation("gotoforest",
                          [Speak("honeyside0",
                                 ["I think TP went deeper into the forest to the right,",
                                  "so I should go that way."])])

sheepconversation = Conversation("sheepconversation",
                                 [Speak("sheepstanding", ["Woah, how'd you know?"], "right"),
                                  Speak("sheepstanding", ["How'd you know I am a sheep and not a rock?"], "right"),
                                  Speak("honeyside0", ["..."], "left"),
                                  Speak("sheepstanding", ["Interaction button? What?",
                                                              "Whatever. Naturally, I suppose you are expecting a dance battle."]),
                                  Speak("honeyside0", ["Wait wha-"]),
                                  Speak("sheepstanding", ["Here we go!", "I'll show you my best moves!"])],
                                 speaksafter = [Speak("sheepstanding", ["Let's go again! I'll show you my best moves!"])])
                                 

tutorialconversation1 = Conversation("tutorialconversation1",
                                     [Speak("honeyback3",
                                            ["Wait...", "You've never done this before, have you."], bottomp=False),
                                      Speak("honeyback3", ["*sigh*"], "left", bottomp = False),
                                      Speak("honeyback3", ["I guess I'll have to teach you."], "left", bottomp = False),
                                      Speak("honeyback3",
                                            ["See those keys down there?",
                                             "There are eight notes, which change octaves automatically."],
                                            "left",
                                            bottomp = False),
                                      Speak("honeyback3",
                                            ["Just press and hold the corresponding key to",
                                             "each note for the duration of the note when it lines up.",
                                             "The better you play, the better I can dance."],
                                            "left", bottomp = False),
                                      Speak("honeyback3",
                                            ["Oh look, a note. I'll tell you when to play it."],
                                            "left", bottomp = False)])

accidentaltutorialintro = Conversation("accidentaltutorialintro",
                                       [Speak("honeyback3", "Woah, what was that?", side="left", bottomp=False),
                                        Speak("honeyback3", "I think it was the dreaded, the terrible, the-", side="left", bottomp=False),
                                        Speak("honeyback3", "ACCIDENTAL!", side="left", bottomp=False),
                                        Speak("honeyback3", ["You better be ready, here comes another one.", "There is a whole new set of keys down there. Take note."],  side="left", bottomp=False)])

holdthis = "You'll want to press and hold \"" + pygame.key.name(variables.settings.keydict["note1"][0]) + "\" now."



pressaspeak = Speak("honeyback3", [holdthis,
                                   "Hold the note until it ends,",
                                   "otherwise you will miss it."], bottomp = False)

pressaspeak.specialexitkeys = ["note1"]

pressanow = Conversation("pressanow",[pressaspeak])


holdthisw = "Hold \"" + pygame.key.name(variables.settings.keydict["note1modified"][0]) + "\" now."

presswspeak = Speak("honeyback3", [holdthisw], bottomp = False)

presswspeak.specialexitkeys = ["note1modified"]

presswnow = Conversation("presswnow",[presswspeak])

releaseaspeak = Speak("honeyback3", ["Alright, release the key now."], bottomp = False)
releaseaspeak.specialexitkeys = ["note1"]
releaseaspeak.releaseexit = True

releaseanow = Conversation("releaseanow",[releaseaspeak])

releasedearlyspeak = Speak("honeyback3", ["You released too early.",
                                          "Hold the note until the end."], bottomp = False)
releasedearlyagainspeak = Speak("honeyback3", ["You released too early... again."], bottomp = False)
releasedearlyspeak.specialexitkeys = ["note1"]
releasedearlyagainspeak.specialexitkeys = ["note1"]

releasedearly = Conversation("releasedearly",[releasedearlyspeak], speaksafter = [releasedearlyagainspeak])

# releasedw version
releasewspeak = Speak("honeyback3", ["Alright, release the key now."], bottomp = False)
releasewspeak.specialexitkeys = ["note1modified"]
releasewspeak.releaseexit = True

releasewnow = Conversation("releasewnow",[releasewspeak])

releasedwearlyspeak = Speak("honeyback3", ["You released too early.",
                                          "Hold the note until the end."], bottomp = False)
releasedwearlyagainspeak = Speak("honeyback3", ["You released too early again."], bottomp = False)
releasedwearlyspeak.specialexitkeys = ["note1modified"]
releasedwearlyagainspeak.specialexitkeys = ["note1modified"]

releasedwearly = Conversation("releasedwearly",[releasedwearlyspeak], speaksafter = [releasedwearlyagainspeak])



endtutorial = Conversation("endtutorial",
                           [Speak("honeyback3",
                                  ["It seems like you get the idea.",
                                   "The dance battle's going to start now, so I'll leave you to it."], bottomp = False)])

prettygood = Conversation("prettygood",
                          [Speak("honeyback3",
                                 ["Hey, that wasn't bad, for your first song.",
                                  "Let's go find TP."])])



letsflee = Conversation("letsflee",
                        [Speak("honeyback3",
                               ["We're just going to run?"]),
                         Speak("honeyback3",
                               ["Fine, let's go."],
                               "left"),
                         Speak("meangreen0", ["Coward! I'd chase you, but I'm stuck to this tree."], "right")])

want2gospeak = Speak("meangreen0", ["Want to have a go?"], options = ["yes", "no"])
want2go = Conversation("want2go",[want2gospeak])

kewlcornyo = Conversation("kewlcornyo",[Speak("kewlcorn0", ["Yo!"])])

chimneytalk = Conversation("chimneytalk",[Speak("flyingchimney4", ["..."])])

losetochimney = Conversation("losetochimney", [Speak("honeyback3",
                                                     ["We lost to my own chimney..."])])

tpboss1 = Conversation("tpboss1", [Speak("honeyside0", ["...", "Tp, what are you doing?"]),
                                   Speak("tpwalksright0", ["I'm dancing, what else?"]),
                                   Speak("honeyside0", ["Never mind.", "Give me my lunch."]),
                                   Speak("tpwalksright0", ["I will... as soon as you get good.",
                                                           "In the mean time, beat my friend here."])])

scarysteve = Conversation("scarysteve", [Speak("scarysteven00", ["Let's dance, bear."])])
steveloses = Conversation("steveloses", [Speak("scarysteven00", ["You win. Take this.",
                                                                "By now, TP has danced his way to the cold forest."])])

steveagain = Conversation("steveagain", [Speak("scarysteven00", ["Let's dance again."], options = ["yes", "no"])])

trophyspeak = Speak("trophy",
                    ["Congradulations!",
                     "This concludes the demo version of Bearly Dancing.",
                     "Game by Oliver Flatt",
                     "Art by Sophia Flatt",
                     "Thanks to: Dad, Mom",
                     "Jacob Valero, James Scholz, and Tessa McNamee for supporting me.",
                     "Finally, thanks to you the player.",
                     "Please give as much feedback as possible to: oflatt@gmail.com",
                     "In bug reports, please give the situation and any error message recieved.",
                     "(spam action)", ".               ", " .              ",
                     "  .             ", "   .            ", "    .           ",
                     "     .          ","      .         ", "       .        ",
                     "        .       ", "         .      ", "          .     ","           .    ", "            .   ",
                     "             .  ", "              . ", "               .", "              . ",
                     "            .   ", "          .     ", "        .       ","      .         ",
                     "    .           ", "  .             ", ".               ", " .              ",
                     "  .             ", "   .            ", "    .           ", "     .          ",
                     "      .         ", "       .        ", "        .       ", "         .      ",
                     "          .     ", "           .    ", "            .   ", "             .  ",
                     "              . ", "               .", "              . ", "            .   ",
                     "          .     ","        .       ","      .         ","    .           ",
                     "  .             ",".               ","!               "])

trophyc = Conversation("trophyc", [trophyspeak],
                       [Speak("trophy", ["Play again with a higher difficulty!",
                                         "To start again, move or rename the save0 folder,",
                                         "Located in the same directory as the bearly dancing executable."])])

beatkewlc = Conversation("beatkewl", [Speak("kewlcorn0", ["Wow, that was cool!",
                                                          "This is cool too, you can have it."])])

beatchimneyc = Conversation("beatchimney", [Speak("flyingchimney4", ["...",
                                                                     "*The chimney drops something.*"])])


hoppingtree = Conversation("hoppingtree", [Speak("chicking0", ["!", "!"])])

# floating conversations #########################################################
floatingconversations = {}

def addfloating(c):
    floatingconversations[c.name] = c
addfloating(tutorialconversation1)
addfloating(pressanow)
addfloating(endtutorial)
addfloating(releaseanow)
addfloating(releasedearly)

addfloating(accidentaltutorialintro)
addfloating(presswnow)
addfloating(releasewnow)
addfloating(releasedwearly)

addfloating(losetochimney)
addfloating(letsflee)



    
# copy them so one save does not alter all the conversations
def getconversation(varname):
    g = globals()
    c = deepcopy(g[varname])
    return c

# this is the conversation object currently being displayed
currentconversation = Conversation("placeholder", [])
