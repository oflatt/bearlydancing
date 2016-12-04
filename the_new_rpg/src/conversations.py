#!/usr/bin/python
#Spirit and Jacob work on script
from graphics import GR
from Conversation import Conversation
from Speak import Speak

longtestdialogue = ["bla", "bla", "a", "monster", "did", "do", "that", "really", "good", "dancin", "he was honey"]
shorttestdialoge = ["I talk just a little"]

testconversation = Conversation([Speak(GR["honeyside0"], longtestdialogue),
                                 Speak(GR["honeyside0"], shorttestdialoge),
                                 Speak(GR["honeyside0"], longtestdialogue),
                                 Speak(GR["honeyside0"], shorttestdialoge)])

ohhoney = ["Honey: Oh goody its lunch, I'm STARVING!",
           "Oh no, I left my glorious spinach-mushroom-provalone-",
           "bacon-broccoli quiche in the forest!",
           "I'll have to go get it."]
ohtp = ["Trash Panda: But Honey, those forests are infested with monsters!",
        "You shouldn't fight all of them just for a quiche!",]
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
ohhoney4 = ["It's me, Honey! I'm just here to get my quiche."]
monster2 = ["No one may pass!"]
ohhoney5 = ["So what.......do you want me to fight you??"]
monster3 = ["No! I want to have a DANCE-OFF with you!"]
ohhoney6 = ["Well that's a relief. I'm way better at dancing than fighting..."]

jeremy = Conversation([Speak(GR["jeremy0"], ["Howdey, Honey",
                                             "Have a random piece of advice.",
                                             "Better dancers live further away from your home for whatever reason.",
                                             "If you don't feel ready to continue, just stick around in one area for a while."])])

#old
secondscene = Conversation([Speak(GR["meangreen0"], monster),
                            Speak(GR["honeyside3"], ohhoney4),
                            Speak(GR["meangreen0"], monster2),
                            Speak(GR["honeyside3"], ohhoney5),
                            Speak(GR["meangreen0"], monster3),
                            Speak(GR["honeyside3"], ohhoney6)])

penultimatefight = Conversation(["Honey: Oh wow, they must be",
                                  "the last boss!",
                                  "Monster: ARGHGHGHGH!",
                                  "Honey: *gulp* Alright, let's go!"])

lastfight = Conversation(["Honey: What, I thought I was done!",
                          "Well, this should be easy.",
                          "Monster: Hehehehehe..."])

finalscene = Conversation(["Honey: *sniff sniff* Finally",
                           "... lunch time."])

currentconversation = testconversation
