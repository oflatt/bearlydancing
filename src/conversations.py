#!/usr/bin/python
# Spirit and Jacob work on script
import variables, pygame
from graphics import GR
from Conversation import Conversation
from Speak import Speak

longtestdialogue = ["bla", "bla", "a", "monster", "did", "do", "that", "really", "good", "dancin", "he was honey"]
shorttestdialoge = ["I talk just a little"]

testconversation = Conversation([Speak(GR["honeyside0"], longtestdialogue),
                                 Speak(GR["honeyside0"], shorttestdialoge),
                                 Speak(GR["honeyside0"], longtestdialogue),
                                 Speak(GR["honeyside0"], shorttestdialoge)])

everyyears = Speak(GR['honeyside0'], ["Every year the same thing. I'm going into hibernation,",
                                      "and TP makes things difficult."])
everyyears.side = 'l'

hungry = Conversation([Speak(GR["honeyside0"], ["I'm hungry...",
                                                "And I have no reason to go outside.",
                                                "Quick lunch, and back to sleep.",
                                                "I'll eat the quiche I made yesterday."])])

thatracoon = Conversation([Speak(GR["honeyside0"], ["That raccoon...", "I knew he was up to no good yesterday.",
                                                    "Now I have to track him down."]),
                           everyyears])

honeydotspeak = Speak(GR["honeyside3"], ["..."])

ohhoney = ["Honey: Oh goody its lunch, I'm STARVING!",
           "Oh no, I left my glorious spinach-mushroom-provalone-",
           "bacon-broccoli quiche in the forest!",
           "I'll have to go get it."]
ohtp = ["Trash Panda: But Honey, those forests are infested with monsters!",
        "You shouldn't fight all of them just for a quiche!", ]
ohhoney2 = ["It is no ordinary quiche, Trash Panda.",
            "It is my glorious spinach-mushroom-provalone-bacon-broccoli quiche!",
            "Lunch is the most important meal of the day, I need to do this."]
ohtp2 = ["I thought breakfast was the-"]
ohhoney3 = ["Shush, I'm leaving now. Time for adventure!"]

firstscene = Conversation([Speak(GR["honeyside0"], ohhoney),
                           Speak(GR["tp"], ohtp),
                           Speak(GR["honeyside0"], ohhoney2),
                           Speak(GR["tp"], ohtp2),
                           Speak(GR["honeyside0"], ohhoney3)])

monster = ["Greenie Meanie: Who goes there!"]
ohhoney4 = ["You know who it is, Meanie. TP took my quiche and I want it back."]
monster2 = ["No one may pass!"]
ohhoney5 = ["So what...you want to fight?"]
monster3 = ["No! I want to have a DANCE-OFF with you!"]
ohhoney6 = ["Ugh... did TP put you up to this? What'd he promise you?"]
monster4 = ["No... um, nothing!"]
ohhoney7 = ["This isn't going anywhere..."]
ohhoney8 = ["Wait, how long have you been here?", "It looks like you have an instrument there.",
            "Good thing too, I'm in need of a bard to get me through this dance battle here.",
            "You're going to play the tunes."]

jeremy = Conversation([Speak(GR["jeremy0"], ["Howdey, Honey",
                                             "Have a random piece of advice.",
                                             "Better dancers live further away from your home for whatever reason.",
                                             "If you don't feel ready to continue, just stick around in one area for a while."])],
                      [Speak(GR["jeremy0"], ["Your bard is bad, and you might have to make up for it with your dance level",
                                             "... or give your bard a bit of practice.",
                                             "Now bug off."])])

secondscene = Conversation([Speak(GR["meangreen0"], monster),
                            Speak(GR["honeyside3"], ohhoney4),
                            Speak(GR["meangreen0"], monster2),
                            Speak(GR["honeyside3"], ohhoney5),
                            Speak(GR["meangreen0"], monster3),
                            Speak(GR["honeyside3"], ohhoney6),
                            Speak(GR["meangreen0"], monster4),
                            Speak(GR["honeyside3"], ohhoney7),
                            Speak(GR["honeyback3"], ohhoney8, side="right")])

dancelionpass = Conversation([Speak(GR["dancelion0"],
                                    ["Hey, I'll only let you through if you beat me in a dance battle.",
                                     "...Yes I do wait around all day stopping travelers like this, thank you."]),
                              honeydotspeak,
                              Speak(GR["dancelion0"],
                                    ["Wait, you telling me your bard can't play in the key of C minor?",
                                     "Come back when they can."])],
                             [Speak(GR["dancelion0"], ["Come back when your bard can play in the key of C minor.",
                                                       "I only dance to music in that key."])])

sheepconversation = Conversation([Speak(GR["sheepstanding"], ["Woah, how'd you know?"], "right"),
                                  Speak(GR["sheepstanding"], ["How'd you know I am a sheep and not a rock?"], "right"),
                                  Speak(GR["honeyside0"], ["..."], "left"),
                                  Speak(GR["sheepstanding"], ["Interaction button? What?",
                                                              "Whatever. Naturally, I suppose you are expecting a dance battle."]),
                                  Speak(GR["honeyside0"], ["Wait wha-"]),
                                  Speak(GR["sheepstanding"], ["Here we go!", "I'll show you my best moves!"])],
                                 switchthisrock="sheeprock")

tutorialconversation1 = Conversation([Speak(GR["honeyback3"],
                                            ["Wait...", "You've never done this before, have you."], bottomp=False),
                                      Speak(GR["honeyback3"], ["*sigh*"], "left", bottomp = False),
                                      Speak(GR["honeyback3"], ["I guess I'll have to teach you."], "left", bottomp = False),
                                      Speak(GR["honeyback3"],
                                            ["So you only have eight notes.",
                                             "I know, I know, quit complaining, you'll be glad there are only eight."],
                                            bottomp = False),
                                      Speak(GR["honeyback3"],
                                            ["Anyways, where was I...",
                                             "Right, eight notes, eight keys.",
                                             "So it's quite simple really, just press and hold the corresponding",
                                             "key to each note for the duration of the note and we'll be good.",
                                             "The better you play, the better I can dance and beat this punk.",
                                             "Oh look, a note, I'll tell you when to play it."],
                                            "right", bottomp = False)])
                                             

holdthis = "Obviously, you'll want to press and hold \"" + pygame.key.name(variables.settings.note1keys[0]) + "\" now."
pressaspeak = Speak(GR["honeyback3"], [holdthis,
                                       "Also, you are going to need to release the key at the end of this note,",
                                       "which is important because notes have length value and you will miss them",
                                       "if you do not hold them for the corrent amount of time."], bottomp = False)
pressaspeak.specialexitkeys = variables.settings.note1keys

pressanow = Conversation([pressaspeak])

currentconversation = testconversation
