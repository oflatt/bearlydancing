#!/usr/bin/python
# Spirit and Jacob work on script
import variables, pygame
from Conversation import Conversation
from Speak import Speak

everyyears = Speak("honeyside0", ["Every year the same thing. I'm going into hibernation,",
                                      "and TP makes things difficult."])
everyyears.side = 'l'

hungry = Conversation([Speak("honeyside0", ["I'm hungry...",
                                            "And I have no reason to go outside.",
                                            "Quick lunch, and back to sleep.",
                                            "I'll eat the quiche I made yesterday."])])

hungryspeak = Speak("honeyside0",["And... I'm still hungry"])

thatracoon = Conversation([Speak("honeyside0", ["That raccoon...",
                                                "I knew he was up to no good yesterday.",
                                                "Now I have to track him down."]),
                           everyyears])

honeydotspeak = Speak("honeyside3", ["..."])

monster = ["Greenie Meanie: Who goes there!"]
ohhoney4 = ["You know who it is, Meanie. TP took my quiche and I want it back."]
monster2 = ["No one may pass!"]
ohhoney5 = ["So what...you want to fight?"]
monster3 = ["No, Honey, you're a bear.", "We'll settle this with a DANCE-OFF!"]
ohhoney6 = ["Did TP put you up to this?"]
monster4 = ["No..."]
ohhoney7 = ["I knew it."]
ohhoney8 = ["Hey, who are you? You've been here the whole time.",
            "User, is it? You have an instrument.",
            "Good thing too, because I'm in need of a bard to get me through this dance battle.",
            "Play the tunes, will you?"]

jeremy = Conversation([Speak("jeremy0", ["Howdey, Honey",
                                         "Have a random piece of advice.",
                                         "Better dancers live further away from your home for whatever reason.",
                                         "If you don't feel ready to continue, just stick around in one area for a while."])],
                      [Speak("jeremy0", ["Your bard is bad, and you might have to make up for it with your dance level",
                                         "... or give your bard a bit of practice.",
                                         "Now bug off."])])

meaniestops = Conversation([Speak("meangreen0", monster),
                            Speak("honeyside3", ohhoney4),
                            Speak("meangreen0", monster2),
                            Speak("honeyside3", ohhoney5),
                            Speak("meangreen0", monster3),
                            Speak("honeyside3", ohhoney6),
                            Speak("meangreen0", monster4),
                            Speak("honeyside3", ohhoney7),
                            Speak("honeyback3", ohhoney8, side="right")],
                           [Speak("honeyback3", ["Here we go again..."])])

dancelionpass = Conversation([Speak("dancelion0",
                                    ["Hey, I'll only let you through if you beat me in a dance battle.",
                                     "...Yes I do wait around all day stopping travelers like this, thank you."]),
                              honeydotspeak,
                              Speak("dancelion0",
                                    ["Wait, you telling me your bard can't play in the key of C minor?",
                                     "Come back when they can."])],
                             [Speak("dancelion0", ["Come back when your bard can play in the key of C minor.",
                                                       "I only dance to music in that key."])])

gotoforest = Conversation([Speak("honeyside0",
                                 ["I think TP went deeper into the forest to the right,",
                                  "so I should go that way."])])

sheepconversation = Conversation([Speak("sheepstanding", ["Woah, how'd you know?"], "right"),
                                  Speak("sheepstanding", ["How'd you know I am a sheep and not a rock?"], "right"),
                                  Speak("honeyside0", ["..."], "left"),
                                  Speak("sheepstanding", ["Interaction button? What?",
                                                              "Whatever. Naturally, I suppose you are expecting a dance battle."]),
                                  Speak("honeyside0", ["Wait wha-"]),
                                  Speak("sheepstanding", ["Here we go!", "I'll show you my best moves!"])],
                                 speaksafter = [Speak("sheepstanding", ["Let's go again! I'll show you my best moves!"])],
                                 switchthisrock="sheeprock")

tutorialconversation1 = Conversation([Speak("honeyback3",
                                            ["Wait...", "You've never done this before, have you."], bottomp=False),
                                      Speak("honeyback3", ["*sigh*"], "left", bottomp = False),
                                      Speak("honeyback3", ["I guess I'll have to teach you."], "left", bottomp = False),
                                      Speak("honeyback3",
                                            ["See those keys down there?",
                                             "There are eight notes, which change octaves automatically."],
                                            "left",
                                            bottomp = False),
                                      Speak("honeyback3",
                                            ["It's quite simple, just press and hold the corresponding",
                                             "key to each note for the duration of the note when it lines up.",
                                             "The better you play, the better I can dance."],
                                            "left", bottomp = False),
                                      Speak("honeyback3",
                                            ["Oh look, a note. I'll tell you when to play it."],
                                            "left", bottomp = False)])

holdthis = "Obviously, you'll want to press and hold \"" + pygame.key.name(variables.settings.note1keys[0]) + "\" now."

pressaspeak = Speak("honeyback3", [holdthis,
                                   "Hold the note until it ends,",
                                   "because otherwise you will miss it."], bottomp = False)

pressaspeak.specialexitkeys = variables.settings.note1keys

pressanow = Conversation([pressaspeak])

releaseaspeak = Speak("honeyback3", ["Alright, release the key now."], bottomp = False)
releaseaspeak.specialexitkeys = variables.settings.note1keys
releaseaspeak.releaseexit = True

releaseanow = Conversation([releaseaspeak])

releasedearlyspeak = Speak("honeyback3", ["You released too early.",
                                          "Hold the note until the end."], bottomp = False)
releasedearlyagainspeak = Speak("honeyback3", ["You released too early... again."], bottomp = False)
releasedearlyspeak.specialexitkeys = variables.settings.note1keys
releasedearlyagainspeak.specialexitkeys = variables.settings.note1keys

releasedearly = Conversation([releasedearlyspeak], speaksafter = [releasedearlyagainspeak])

endtutorial = Conversation([Speak("honeyback3",
                                  ["Alright, it seems like you get the idea.",
                                   "The dance battle's going to start now, so I'll leave you to it."], bottomp = False)])

prettygood = Conversation([Speak("honeyback3",
                                 ["Hey, that wasn't bad, for your first song.",
                                  "I think I'll hire you as my bard. I have a feeling you'll be needed again.",
                                  "Let's go."])])

letsflee = Conversation([Speak("honeyback3",
                               ["We're just going to run?"]),
                         Speak("honeyback3",
                               ["Fine, but you better stick around... who knows who will challenge me to a dance battle next."],
                               "left"),
                         Speak("meangreen0", ["Coward! I'd chase you but I'm stuck to this tree."], "right")])

want2gospeak = Speak("meangreen0", ["Want to have a go?"], options = ["yes", "no"])
want2go = Conversation([want2gospeak])

kewlcornyo = Conversation([Speak("kewlcorn0", ["Yo!"])])

currentconversation = None
